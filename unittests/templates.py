import os
from pathlib import Path
from typing import Dict

import jinja2

HERE = Path(os.path.dirname(__file__))

_templates = jinja2.Environment(loader=jinja2.FileSystemLoader(str(HERE / "templates")))


def render_template(template_path: Path, context=Dict[str, str]) -> str:
    template = _templates.get_template(str(template_path))
    return template.render(**context)
