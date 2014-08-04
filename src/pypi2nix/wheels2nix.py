import os
import json


def do(wheels_file='generated.wheels', nix_file='generated.nix',
       nix_path=''):

    if nix_path != '':
        nix_path = '-I ' + nix_path


    wheels = []
    for wheel in open(wheels_file).read().split('\n'):
        if not wheel:
            continue

        dist_folder = '%s/lib/%s/site-packages' % (
            wheel,
            wheel.split('-')[1],
            )
        dist_info = [
            i for i in os.listdir(dist_folder)
            if i.endswith('.dist-info')
            ][0]
        wheels.append('%s/%s/metadata.json' % (dist_folder, dist_info))

    dists_meta = [json.load(open(item)) for item in wheels]
    dists_names = [item['name'] for item in dists_meta]

    generated = 'python: self:\n{\n\n'
    for meta in dists_meta:
        requires = []
        if 'run_requires' in meta:
            for item in meta['run_requires']:
                if 'requires' in item:
                    for req_item in item['requires']:
                        dist_name = req_item.split(' ')[0]
                        if dist_name in dists_names:
                            requires.append(dist_name)
        if 'summary' in meta:
            generated += '  "{}".meta.description = "{}";\n'.format(
                meta['name'], meta['summary'])
        if 'extensions' in meta and \
           'python.details' in meta['extensions'] and \
           'project_urls' in meta['extensions']['python.details'] and \
           'Home' in meta['extensions']['python.details']['project_urls']:
            generated += '  "{}".meta.homepage = "{}";\n'.format(
                meta['name'],
                meta['extensions']['python.details']['project_urls']['Home'],
                )
        if 'license' in meta:
            generated += '  "{}".meta.license = "{}";\n'.format(
                meta['name'], meta['license'])
        generated += '  "{}".requires = [ {} ];\n\n'.format(
            meta['name'],
            ' '.join(['self.' + i for i in requires]),
            )
    generated += '}'

    open(nix_file, 'wb').write(generated)

    return nix_file
