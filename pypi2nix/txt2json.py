import os
import json

from pip.download import PipSession
from pip.index import PackageFinder
from pip.req import parse_requirements


def do(txt_file, json_file='generated.json'):
    print '-> generating: generated.json'

    results = {}
    if os.path.exists(json_file):
        print '  -> loading existing {}'.format(json_file)
        results = json.load(open(json_file))

    session = PipSession()

    finder = PackageFinder(
        find_links=[],
        index_urls=['https://pypi.python.org/simple/'],
        allow_all_external=True,
        use_wheel=False,
        session=session
    )

    print '  -> reading {}'.format(txt_file)
    reqs = parse_requirements(txt_file, finder, session=session)

    print '  -> proccessing every specification in {}'.format(txt_file)
    for req in reqs:
        spec_name = str(req.__dict__['req']).replace('==', '-')
        if spec_name in results:
            print '    -> {} already in {}'.format(spec_name, json_file)
        else:
            print '    -> {} getting info'.format(spec_name)
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

    print '  -> done'
    return json_file
