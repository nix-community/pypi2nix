import os
import stat
import shlex
import hashlib
import datetime
import tempfile
import itertools
import subprocess


NIX_BUILDOUT = '''with (import <nixpkgs> {});
stdenv.mkDerivation {
  name = "%(name)s";
  buildInputs = [ %(buildInputs)s pkgs.python27Packages.zc_buildout_nix ];
  __noChroot = true;
  buildCommand = ''
    # %(timestamp)s
    unset http_proxy
    unset ftp_proxy
    cat > buildout.cfg <<EOF
    [buildout]
    extends = %(extends)s
    eggs-directory = %(eggsdir)s
    versions = versions
    parts = deps

    [deps]
    recipe = zc.recipe.egg
    eggs =
        %(eggs)s

    [versions]
    %(versions)s
    EOF
    ${pkgs.python27Packages.zc_buildout_nix}/bin/buildout-nix -q
    sed -i -e 's@self.name = specification.project_name.lower()@self.name, self.project_name = specification.project_name.lower(), specification.project_name@g' %(eggsdir)s/tl.eggdeps*/tl/eggdeps/graph.py
    sed -i -e 's@name_string = "%%s %%s" %% (node.name, node.dist.version)@name_string = "%%s %%s" %% (node.project_name, node.dist.version)@g' %(eggsdir)s/tl.eggdeps*/tl/eggdeps/plaintext.py
    sed -i -e 's@name_string = node.name@name_string = node.project_name@g' %(eggsdir)s/tl.eggdeps*/tl/eggdeps/plaintext.py
    bin/eggdeps -nt %(specifications)s > $out
    echo "### --- ###" >> $out
    cat bin/eggdeps >> $out
  '';
}
'''


class Buildout(object):

    def __init__(self, config):
        self.name = config['name']
        self.environment = config['environment']
        self.buildInputs = config.get('buildInputs', [])
        self.eggs = config.get('eggs', '')
        self.extends = config.get('extends', '')
        self.versions = config.get('versions', [])
        self.doCheck = config.get('doCheck', True)
        self.override = config.get('override', {})
        self.installCommand = config.get('installCommand',
            'easy_install --always-unzip --prefix="$out" .')
        self.extra_dependencies = list(set(itertools.chain(*([
            [tmp for tmp in item['buildInputs']
            if not tmp.startswith('python.modules.') and
               not tmp.startswith('pkgs.')]
            for item in self.override.values()
            if 'buildInputs' in item
        ] + [
            [tmp for tmp in item['propagatedBuildInputs']
            if not tmp.startswith('python.modules.') and
               not tmp.startswith('pkgs.')]
            for item in self.override.values()
            if 'propagatedBuildInputs' in item
        ]))))

    def run(self, eggsdir='eggs'):
        buildout_dir = tempfile.mkdtemp(
            prefix='pypi2nix-buildout-%s-' % self.name)
        os.chmod(eggsdir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                 stat.S_IXOTH | stat.S_IROTH | stat.S_IWOTH)
        f = open(buildout_dir + '/default.nix', 'w+')
        _hash = hashlib.md5()
        _hash.update(str(self.name))
        _hash.update(str(self.extends))
        _hash.update(str(self.extra_dependencies))
        _hash.update(str(self.versions))
        f.write(NIX_BUILDOUT % {
            'name': 'pypi2nix-%s-%s' % (self.name, self.environment),
            'buildInputs': ' '.join(['wget'] + self.buildInputs),
            'timestamp': '%s - %s' % (
                datetime.datetime.now().strftime('%Y-%m-%d'),
                _hash.hexdigest()),
            'extends': self.extends,
            'eggsdir': eggsdir,
            'eggs': '\n        '.join(
                ['tl.eggdeps', self.name] + self.extra_dependencies),
            'versions': '\n    '.join(self.versions),
            'specifications': ' '.join(
                [self.name] + self.extra_dependencies),
        })
        f.close()
        output = subprocess.check_output(
            shlex.split('/run/current-system/sw/bin/nix-build'),
            cwd=buildout_dir, shell=True
        )
        return self.parse_buildout_result(open(output.strip()).read())

    def parse_buildout_result(self, text):
        lines = text.split('### --- ###')[0].strip().split('\n')
        paths = text.split('### --- ###')[1].split('sys.path[0:0] = [\n')[1]
        paths = paths.split('\n  ]\n\nimport tl.eggdeps.cli')[0].split('\n')
        paths = [i.strip().strip(',').strip("'") for i in paths]

        tmp_result, parents, previous = {}, [None], None
        for line in lines:
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

            if level == 0:
                parents = [None]
            elif level > previous_level:
                parents.append(previous)
            elif level < previous_level:
                parents = parents[:-1*(previous_level - level)]

            parent = parents[-1]
            if parent:
                parent_stripped_split = parent.strip().split()
                tmp_result.setdefault(parent_stripped_split[0], {})
                tmp_result[parent_stripped_split[0]].setdefault('extras', [])
                tmp_result[parent_stripped_split[0]].setdefault(
                    'dependencies', [])
                tmp_result[parent_stripped_split[0]]['dependencies'].append(
                    stripped_line_split[0])

            # collect data
            if (len(line) - len(stripped_line)) % 4 == 0:
                tmp_result.setdefault(stripped_line_split[0], {})
                tmp_result[stripped_line_split[0]].setdefault('extras', [])
                tmp_result[stripped_line_split[0]].setdefault(
                    'dependencies', [])
                tmp_result[stripped_line_split[0]]['version'] = \
                    stripped_line_split[1]

            previous = line

        def get_path(name):
            for path in paths:
                if name in path:
                    return path

        result = {}
        for name, data in tmp_result.items():
            result[self.fullname(name, tmp_result)] = {
                'name': name,
                'version': data['version'],
                'path': get_path(name),
                'buildInputs': (
                    name in self.override and
                    'buildInputs' in self.override[name]
                ) and [
                    self.fullname(i, tmp_result)
                    for i in self.override[name]['buildInputs']
                ] or [],
                'propagatedBuildInputs': [
                    self.fullname(k, tmp_result)
                    for k in (
                        data['dependencies'] + ((
                            name in self.override and
                            'propagatedBuildInputs' in self.override[name]
                        )
                            and self.override[name]['propagatedBuildInputs']
                            or []
                        ))
                ],
                'doCheck': (
                    name in self.override and
                    'doCheck' in self.override[name])
                and str(self.override[name]['doCheck']).lower()
                or str(self.doCheck).lower(),

                'configurePhase': (
                    name in self.override and
                    'configurePhase' in self.override[name])
                and self.override[name]['configurePhase']
                or None,
                'installCommand': self.installCommand
            }

        self.remove_circural_dependencies(
            result, self.fullname(self.name, tmp_result))
        return result

    def fullname(self, name, data):
        if name.startswith('python.modules.') or \
           name.startswith('pkgs.'):
            return name
        data = data[name]
        return '%s%s-%s' % (
            name,
            len(data['extras']) and '__%s' % '_'.join(data['extras']) or '',
            data['version'])

    def remove_circural_dependencies(self, result, to_check, parents=[]):
        if not hasattr(self, 'checked'):
            self.checked = []
        propagatedBuildInputs = []
        for item in result[to_check]['propagatedBuildInputs']:
            if item.startswith('python.modules.') or \
               item.startswith('pkgs.'):
                continue
            if item in parents:
                continue
            if item not in self.checked:
                self.remove_circural_dependencies(
                    result, item, parents + [to_check])
            propagatedBuildInputs.append(item)

        if result[to_check]['propagatedBuildInputs'] != propagatedBuildInputs:
            result[to_check]['installCommand'] = \
                'easy_install --always-unzip --no-deps --prefix="$out" .'
        result[to_check]['propagatedBuildInputs'] = propagatedBuildInputs

        self.checked.append(to_check)


def run_buildout(eggsdir, config):
    buildout = Buildout(config)
    return buildout.run(eggsdir)
