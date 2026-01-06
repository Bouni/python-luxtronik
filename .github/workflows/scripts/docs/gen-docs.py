#!/usr/bin/env python
import logging
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

from luxtronik import (
    Calculations,
    Parameters,
    Visibilities,
    Holdings,
    Inputs,
)
from luxtronik.datatypes import (
    SelectionBase,
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("docs generator")


BASEPATH = Path(__file__).resolve().parent


def get_items(definitions):
    items = []
    for d in definitions:
        desc = d.description
        if issubclass(d.data_type, SelectionBase):
            desc += "\nUser-Options: " + ", ".join(d.data_type.options())
        items.append({
            "number": d.index,
            "type": definitions.name,
            "name": d.name,
            "unit": d.data_type.unit,
            "description": desc,
        })
    return items


def gather_data() -> dict:
    logger.info("gather docs data")
    data = {}
    data["parameters"] = get_items(Parameters.definitions)
    data["calculations"] = get_items(Calculations.definitions)
    data["visibilities"] = get_items(Visibilities.definitions)
    data["holdings"] = get_items(Holdings.definitions)
    data["inputs"] = get_items(Inputs.definitions)
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
