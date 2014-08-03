import os
import pypi2nix.cmd


def do(wheels_file='generated.wheels', nix_file='generated.nix',
       nix_path=''):

    if nix_path != '':
        nix_path = '-I ' + nix_path

    command = 'unveil create-meta'
    for wheel in open(wheels_file).read().split('\n'):
        if wheel:
            folder = '%s/lib/%s/site-packages' % (
                wheel,
                wheel.split('-')[1],
                )
            dist_info = [
                i for i in os.listdir(folder)
                if i.endswith('.dist-info')
                ][0]
            command += ' --dist=%s/%s' % (folder, dist_info)

    out, err = pypi2nix.cmd.do(command)
    if err:
        raise Exception(err)

    open(nix_file, 'wb').write(out)

    return nix_file
