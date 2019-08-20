import os
import shlex
import sys
from typing import Iterable

import jinja2
from setuptools._vendor.packaging.utils import canonicalize_name

from pypi2nix.logger import Logger
from pypi2nix.overrides import AnyOverrides
from pypi2nix.sources import Sources
from pypi2nix.wheel import Wheel

HERE = os.path.dirname(__file__)


def main(
    packages_metadata: Iterable[Wheel],
    sources: Sources,
    requirements_name: str,
    requirements_frozen: str,
    extra_build_inputs: Iterable[str],
    enable_tests: bool,
    python_version: str,
    current_dir: str,
    logger: Logger,
    common_overrides: Iterable[AnyOverrides] = [],
) -> None:
    """Create Nix expressions.
    """

    default_file = os.path.join(current_dir, "{}.nix".format(requirements_name))
    overrides_file = os.path.join(
        current_dir, "{}_override.nix".format(requirements_name)
    )
    frozen_file = os.path.join(current_dir, "{}_frozen.txt".format(requirements_name))

    version_file = os.path.join(os.path.dirname(__file__), "VERSION")
    with open(version_file) as f:
        version = f.read()
    version = version.strip()

    metadata_by_name = {x.name: x for x in packages_metadata}

    generated_packages_metadata = []
    for item in sorted(packages_metadata, key=lambda x: x.name):
        if item.build_dependencies:
            buildInputs = "\n".join(
                sorted(
                    [
                        '        self."{}"'.format(name)
                        for name in item.build_dependencies
                    ]
                )
            )
            buildInputs = "[\n" + buildInputs + "\n      ]"
        else:
            buildInputs = "[ ]"
        propagatedBuildInputs = "[ ]"
        if item.deps:
            deps = [
                canonicalize_name(x)
                for x in item.deps
                if canonicalize_name(x) in metadata_by_name.keys()
            ]
            if deps:
                propagatedBuildInputs = "[\n%s\n      ]" % (
                    "\n".join(
                        sorted(
                            [
                                '        self."%s"' % (metadata_by_name[x].name)
                                for x in deps
                                if x != item.name
                            ]
                        )
                    )
                )
        source = sources[item.name]
        fetch_expression = source.nix_expression()
        generated_packages_metadata.append(
            dict(
                name=item.name,
                version=item.version,
                fetch_expression=fetch_expression,
                buildInputs=buildInputs,
                propagatedBuildInputs=propagatedBuildInputs,
                homepage=item.homepage,
                license=item.license,
                description=item.description,
            )
        )

    templates = jinja2.Environment(loader=jinja2.FileSystemLoader(HERE + "/templates"))

    generated_template = templates.get_template("generated.nix.j2")
    generated = "\n\n".join(
        generated_template.render(**x) for x in generated_packages_metadata
    )

    overrides = templates.get_template("overrides.nix.j2").render()

    common_overrides_expressions = [
        "    (" + override.nix_expression(logger) + ")" for override in common_overrides
    ]

    default_template = templates.get_template("requirements.nix.j2")
    overrides_file_nix_path = os.path.join(".", os.path.split(overrides_file)[1])
    default = default_template.render(
        version=version,
        command_arguments=" ".join(map(shlex.quote, sys.argv[1:])),
        python_version=python_version,
        extra_build_inputs=(
            extra_build_inputs
            and "with pkgs; [ %s ]" % (" ".join(extra_build_inputs))
            or "[]"
        ),
        overrides_file=overrides_file_nix_path,
        enable_tests=str(enable_tests).lower(),
        generated_package_nix=generated,
        common_overrides="\n".join(common_overrides_expressions),
        paths_to_remove="paths_to_remove.remove(auto_confirm)",
        self_uninstalled="self.uninstalled = paths_to_remove",
        python_major_version=python_version.replace("python", "")[0],
    )

    if not os.path.exists(overrides_file):
        with open(overrides_file, "w+") as f:
            f.write(overrides.strip())
            logger.info("|-> writing %s" % overrides_file)

    with open(default_file, "w+") as f:
        f.write(default.strip())

    with open(frozen_file, "w+") as f:
        f.write(requirements_frozen)
