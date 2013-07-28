import os
import stat
import shlex
import datetime
import tempfile
import subprocess


NIX_BUILDOUT = '''with (import <nixpkgs> {});
stdenv.mkDerivation {
  name = "pypi2nix-%(name)s-%(environment)s";
  buildInputs = [ wget %(buildInputs)s ];
  __noChroot = true;
  buildCommand = ''
    # %(timestamp)s
    unset http_proxy
    unset ftp_proxy
    wget https://raw.github.com/buildout/buildout/master/bootstrap/bootstrap.py
    cat > buildout.cfg <<EOF
    [buildout]
    extends = %(extends)s
    eggs-directory = %(eggsdir)s
    versions = versions
    parts = deps

    [deps]
    recipe = zc.recipe.egg
    eggs =
        tl.eggdeps
        %(name)s
        %(eggs)s

    [versions]
    %(versions)s
    EOF
    python bootstrap.py
    bin/buildout -q
    sed -i -e 's@self.name = specification.project_name.lower()@self.name, self.project_name = specification.project_name.lower(), specification.project_name@g' /home/rok/.buildout/eggs/tl.eggdeps*/tl/eggdeps/graph.py
    sed -i -e 's@name_string = "%%s %%s" %% (node.name, node.dist.version)@name_string = "%%s %%s" %% (node.project_name, node.dist.version)@g' %(eggsdir)s/tl.eggdeps*/tl/eggdeps/plaintext.py
    sed -i -e 's@name_string = node.name@name_string = node.project_name@g' %(eggsdir)s/tl.eggdeps*/tl/eggdeps/plaintext.py
    bin/eggdeps -nt %(name)s > $out
  '';
}
'''


class Buildout(object):

    def __init__(self, config):
        self.name = config['name']
        self.environment = config['environment']
        self.eggs = config.get('eggs', '')
        self.extends = config.get('extends', '')
        self.versions = config.get('versions', [])
        self.buildInputs = config.get('buildInputs', [])

    def run(self, eggsdir='eggs'):
        buildout_dir = tempfile.mkdtemp(
            prefix='pypi2nix-buildout-%s-' % self.name)
        os.chmod(eggsdir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                 stat.S_IXOTH | stat.S_IROTH | stat.S_IWOTH)
        f = open(buildout_dir + '/default.nix', 'w+')
        f.write(NIX_BUILDOUT % {
            'name': self.name,
            'environment': self.environment,
            'eggs': self.eggs,
            'extends': self.extends,
            'versions': '\n    '.join(self.versions),
            'buildInputs': ' '.join(self.buildInputs),
            'eggsdir': eggsdir,
            'timestamp': datetime.datetime.isoformat(datetime.datetime.now())
        })
        f.close()
        output = subprocess.check_output(
            shlex.split('/run/current-system/sw/bin/nix-build'),
            cwd=buildout_dir, shell=True
        )
        return parse_buildout_result(open(output.strip()).read())


def parse_buildout_result(text):

    tmp_result, parents, previous = {}, [None], None
    for line in text.split('\n'):
        stripped_line = line.strip()
        stripped_line_split = stripped_line.split(' ')
        if len(stripped_line) == 0:
            continue

        # get the level (starting with 0)
        if (len(line) - len(stripped_line)) % 4 == 0:
            level = (len(line) - len(stripped_line)) / 4
        else:
            tmp = parents[-1].strip().split()[0]
            tmp_result.setdefault(tmp, {})
            tmp_result[tmp].setdefault('extras', [])
            tmp_result[tmp].setdefault('dependencies', [])
            tmp_result[tmp]['extras'].append(line.strip()[1:-1])
            continue

        # previous level
        if previous is None:
            previous_level = 0
        elif (len(previous) - len(previous.strip())) % 4 == 0:
            previous_level = (len(previous) - len(previous.strip())) / 4

        if len(parents) == 1:
            parents.append(line)
        if level > previous_level:
            parents.append(previous)
        if level < previous_level:
            parents = parents[:-1*(previous_level - level)]

        parent = parents[-1]
        parent_stripped_split = parent.strip().split()
        tmp_result.setdefault(parent_stripped_split[0], {})
        tmp_result[parent_stripped_split[0]].setdefault('extras', [])
        tmp_result[parent_stripped_split[0]].setdefault('dependencies', [])
        tmp_result[parent_stripped_split[0]]['dependencies'].append(
            stripped_line_split[0])

        # collect data
        if (len(line) - len(stripped_line)) % 4 == 0:
            tmp_result.setdefault(stripped_line_split[0], {})
            tmp_result[stripped_line_split[0]].setdefault('extras', [])
            tmp_result[stripped_line_split[0]].setdefault('dependencies', [])
            tmp_result[stripped_line_split[0]]['version'] = \
                stripped_line_split[1]

        previous = line
        if len(parents) == 1:
            parents.append(line)

    result = {}
    for name, data in tmp_result.items():
        result['%s%s-%s' % (
            name,
            len(data['extras']) and '[%s]' % ','.join(data['extras']) or '',
            data['version']
        )] = {
            'name': name,
            'version': data['version'],
            'dependencies': [
                '%s%s-%s' % (
                    i,
                    len(tmp_result[i]['extras']) and '[%s]' % ','.join(
                       self. tmp_result[i]['extras']) or '',
                    tmp_result[i]['version'])
                for i in data['dependencies']]
        }
    return result


def run_buildout(eggsdir, config):
    buildout = Buildout(config)
    return buildout.run(eggsdir)
