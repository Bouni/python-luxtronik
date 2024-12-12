#!/usr/bin/env python
import logging
import re
from pathlib import Path
from typing import Literal

from jinja2 import Environment, FileSystemLoader, select_autoescape

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("doc-gen")

BASEPATH = Path(__file__).resolve().parent


def parse_group(group: Literal["calculations", "parameters", "visibilities"]) -> list[dict]:
    logger.info("parse group '%s'", group)
    data = []
    with open(BASEPATH.parents[3] / f"luxtronik/{group}.py") as f:
        raw = f.read()
        regex = re.compile(r"(?P<number>\d+):\s+(?P<type>[^(]+)\(\"(?P<name>[^\"]+)\"\)")
        results = [m.groupdict() for m in regex.finditer(raw)]
        logger.info("found %d entries", len(results))
        for r in results:
            data.append({"number": r["number"], "type": r["type"], "name": r["name"]})
    return data


def render_docs():
    logger.info("render docs")
    env = Environment(loader=FileSystemLoader(str(BASEPATH / "templates")), autoescape=select_autoescape())
    template = env.get_template("docs.jinja")
    group_data = {}
    for g in ("calculations", "parameters", "visibilities"):
        group_data[g] = parse_group(g)
    (BASEPATH.parents[3] / "docs").mkdir(exist_ok=True)
    with open(BASEPATH.parents[3] / "docs/index.html", "w", encoding="UTF-8") as f:
        f.write(template.render(data=group_data))


if __name__ == "__main__":
    print(BASEPATH)
    render_docs()
