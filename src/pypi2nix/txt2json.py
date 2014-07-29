import os
import json

from pip.index import PackageFinder
from pip.req import parse_requirements


def do(txt_file, json_file='generated.json'):
    results = {}
    if os.path.exists(json_file):
        results = json.load(open(json_file))

    finder = PackageFinder(
        find_links=[],
        index_urls=['https://pypi.python.org/simple/'],
        allow_all_external=True,
        use_wheel=False
    )
    reqs = parse_requirements(txt_file, finder)

    for req in reqs:
        print '  -> {}'.format(req.name)
        if req.name not in results:
            link = finder.find_requirement(req, False)
            results.update({
                req.name: {
                    "name": str(req.__dict__['req']).replace('==', '-'),
                    link.hash_name: link.hash,
                    "url": link.url_without_fragment
                }})

    json.dump(results, open(json_file, 'wb+'))
