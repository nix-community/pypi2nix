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
    bin/buildout
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
        return {
            self.name: open(output.strip()).read()
        }


def run_buildout(eggsdir, config):
    buildout = Buildout(config)
    return buildout.run(eggsdir)
