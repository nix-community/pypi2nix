import os
import sys

import click
import jinja2

HERE = os.path.dirname(__file__)


def main(packages_metadata,
         requirements_name,
         requirements_files,
         requirements_frozen,
         extra_build_inputs,
         enable_tests,
         python_version,
         current_dir,
         common_overrides=[],
         ):
    '''Create Nix expressions.
    '''

    default_file = os.path.join(
        current_dir, '{}.nix'.format(requirements_name)
    )
    overrides_file = os.path.join(
        current_dir, '{}_override.nix'.format(requirements_name)
    )
    frozen_file = os.path.join(
        current_dir, '{}_frozen.txt'.format(requirements_name)
    )

    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    with open(version_file) as f:
        version = f.read()

    metadata_by_name = {x['name'].lower(): x for x in packages_metadata}

    generated_packages_metadata = []
    for item in sorted(packages_metadata, key=lambda x: x['name']):
        propagatedBuildInputs = '[ ]'
        if item.get('dependencies'):
            deps = [x for x in item['dependencies']
                    if x.lower() in metadata_by_name.keys()]
            if deps:
                propagatedBuildInputs = "[\n%s\n    ]" % (
                    '\n'.join(sorted(
                        ['      self."%s"' %
                         (metadata_by_name[x.lower()]['name'])
                         for x in deps if x not in [item['name']]]
                    )))
        fetch_type = item.get('fetch_type', None)
        if fetch_type == 'path':
            fetch_expression = ('pkgs.lib.cleanSource ./' +
                                os.path.relpath(item['url'], current_dir))
        elif fetch_type == 'fetchgit':
            fetch_expression = 'pkgs.fetchgit { url = "%(url)s"; '\
                '%(hash_type)s = "%(hash_value)s"; rev = "%(rev)s"; }' % dict(
                    url=item['url'],
                    hash_type=item['hash_type'],
                    hash_value=item['hash_value'],
                    rev=item['rev']
                )
        elif fetch_type == 'fetchhg':
            fetch_expression = 'pkgs.fetchhg { url = "%(url)s"; '\
                '%(hash_type)s = "%(hash_value)s"; rev = "%(rev)s"; }' % dict(
                    url=item['url'],
                    hash_type=item['hash_type'],
                    hash_value=item['hash_value'],
                    rev=item['rev']
                )
        else:
            fetch_expression = 'pkgs.fetchurl { url = "%(url)s"; '\
                '%(hash_type)s = "%(hash_value)s"; }' % dict(
                    url=item['url'],
                    hash_type=item['hash_type'],
                    hash_value=item['hash_value'],
                )

        generated_packages_metadata.append(dict(
            name=item.get("name", ""),
            version=item.get("version", ""),
            fetch_expression=fetch_expression,
            propagatedBuildInputs=propagatedBuildInputs,
            homepage=item.get("homepage", ""),
            license=item.get("license", ""),
            description=item.get("description", ""),
        ))

    templates = jinja2.Environment(
        loader=jinja2.FileSystemLoader(HERE + '/templates'),
    )

    generated_template = templates.get_template('generated.nix.j2')
    generated = '\n\n'.join(
        generated_template.render(**x) for x in generated_packages_metadata
    )

    overrides = templates.get_template('overrides.nix.j2').render()

    common_overrides_expressions = [
        '    (' + override.nix_expression() + ')'
        for override in common_overrides
    ]

    default_template = templates.get_template('requirements.nix.j2')
    overrides_file_nix_path = \
        os.path.join(
            '.',
            os.path.split(
                overrides_file
            )[1]
        )
    default = default_template.render(
        version=version,
        command_arguments=' '.join(sys.argv[1:]),
        python_version=python_version,
        extra_build_inputs=(
            extra_build_inputs and
            "with pkgs; [ %s ]" % (' '.join(extra_build_inputs)) or
            "[]"
        ),
        overrides_file=overrides_file_nix_path,
        enable_tests=str(enable_tests).lower(),
        generated_package_nix=generated,
        common_overrides='\n'.join(common_overrides_expressions),
        paths_to_remove="paths_to_remove.remove(auto_confirm)",
        self_uninstalled="self.uninstalled = paths_to_remove",
        python_major_version=python_version.replace("python", "")[0],
    )

    if not os.path.exists(overrides_file):
        with open(overrides_file, 'w+') as f:
            f.write(overrides.strip())
            click.echo('|-> writing %s' % overrides_file)

    with open(default_file, 'w+') as f:
        f.write(default.strip())

    with open(requirements_frozen) as f:
        frozen_content = f.read()

    with open(frozen_file, 'w+') as f:
        f.write(frozen_content)
