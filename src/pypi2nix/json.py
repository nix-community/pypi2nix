import json

from pypi2nix.requirement import Requirement


class RequirementEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Requirement):
            return obj.get_release()
        return super.default(self, obj)
