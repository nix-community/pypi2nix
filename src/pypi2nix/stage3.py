
def find_homepage(item):
    if 'extensions' in item and \
            'python.details' in item['extensions'] and \
            'project_urls' in item['extensions']['python.details']:
        homepage = item['extensions']['python.details'].get('Home', '')
    return homepage


def find_license(item):
    license = ''
    if 'license' not in item:
        if item == '"ZPL 2.1':
            item = "lib.zpt21"
    return license


def do(metadata, generate_file):
    metadata_by_name = {x['name']: x for x in metadata}
    # top_level = list(set(metadata.keys()).difference(set(reduce(
    #     lambda x, y: x + y, list(set([x['deps'] for x in metadata]))))))

    with open(generate_file, 'wa+') as f:
        write = lambda x: f.write(x + '\n')

        write("{ pkgs, self, pythonPackages}:")
        write("let")
        write("  inherit (pythonPackages) buildPythonPackage;")
        write("  inherit (pkgs) fetchurl lib;")
        write("in {")

        for item in metadata:
            write('   "%(name)s" = buildPythonPackage {' % item)
            write('     name = "%(name)s-%(version)s";' % item)
            write('     src = fetchurl {')
            write('       url = "%(url)s";' % item)
            write('       md5 = "%(md5)s";' % item)
            write('     };')
            write('     doCheck = false;')
            write('     propagatedBuildInputs = [ %s ];' % ' '.join([
                'self."%(name)s"' % metadata_by_name[x]
                for x in item['deps'] if x in metadata_by_name]))
            write('     meta = {')
            # write('       homepage = "%s"' % find_homepage(item))
            # write('       license = "%s"' % find_license(item))
            # write('       description = "%(sumarry)s"' % item)
            write('     };')
            write('   };')

        write('}')
