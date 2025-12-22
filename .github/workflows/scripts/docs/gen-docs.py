#!/usr/bin/env python
import logging
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

from luxtronik.calculations import Calculations
from luxtronik.parameters import Parameters
from luxtronik.visibilities import Visibilities

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("docs generator")


BASEPATH = Path(__file__).resolve().parent


def gather_data() -> dict:
    logger.info("gather docs data")
    p = Parameters()
    c = Calculations()
    v = Visibilities()
    data = {"parameters": [], "calculations": [], "visibilities": []}
    for number, parameter in p._data.items():
        data["parameters"].append({"number": number, "type": parameter.__class__.__name__, "name": parameter.name})
    for number, calculation in c._data.items():
        data["calculations"].append(
            {"number": number, "type": calculation.__class__.__name__, "name": calculation.name}
        )
    for number, visibility in v._data.items():
        data["visibilities"].append({"number": number, "type": visibility.__class__.__name__, "name": visibility.name})
    return data


def render_docs():
    logger.info("render docs")
    env = Environment(loader=FileSystemLoader(str(BASEPATH / "templates")), autoescape=select_autoescape())
    template = env.get_template("docs.html")
    group_data = gather_data()
    (BASEPATH.parents[3] / "docs").mkdir(exist_ok=True)
    with open(BASEPATH.parents[3] / "docs/index.html", "w", encoding="UTF-8") as f:
        f.write(template.render(data=group_data, now=datetime.now()))


if __name__ == "__main__":
    render_docs()
