import os
import json
import click

from pip.download import PipSession
from pip.index import PackageFinder
from pip.req import parse_requirements


def do(txt_file, json_file='generated.json'):
    click.secho('-> generating: generated.json', fg='cyan')

    results = {}
    if os.path.exists(json_file):
        click.secho('  -> loading existing {}'.format(json_file), fg='cyan')
        results = json.load(open(json_file))

    session = PipSession()

    finder = PackageFinder(
        find_links=[],
        index_urls=['https://pypi.python.org/simple/'],
        allow_all_external=True,
        use_wheel=False,
        session=session
    )

    click.secho('  -> reading {}'.format(txt_file), fg='cyan')
    reqs = parse_requirements(txt_file, finder, session=session)

    click.secho('  -> proccessing every specification in {}'.format(txt_file), fg='cyan')
    for req in reqs:
        spec_name = str(req.__dict__['req']).replace('==', '-')
        if spec_name in results:
            click.secho('    -> {} already in {}'.format(spec_name, json_file), fg='cyan')
        else:
            click.secho('    -> {} getting info'.format(spec_name), fg='cyan')
            link = finder.find_requirement(req, False)
            results.update({
                spec_name: {
                    "name": req.name,
                    "spec_name": spec_name,
                    "hash_name": link.hash_name,
                    "hash": link.hash,
                    "url": link.url_without_fragment
                }})

    json.dump(results, open(json_file, 'wb+'))

    click.secho('  -> done', fg='cyan')
    return json_file
