#! /usr/bin/env python3
# pylint: disable=invalid-name
"""
Script to dump all available smart home interface values from Luxtronik controller.
"""

import logging

from luxtronik.scripts import (
    create_default_args_parser,
    print_dump_header,
    print_dump_row
)
from luxtronik.shi import create_modbus_tcp
from luxtronik.shi.constants import LUXTRONIK_DEFAULT_MODBUS_PORT

logging.disable(logging.CRITICAL)

def dump_fields(read_cb):
    data_vector = read_cb()
    print_dump_header(f"{data_vector.name}s")
    for definition, field in data_vector.items():
        print_dump_row(definition.index, field)

def dump_shi():
    parser = create_default_args_parser(
        "Dumps all smart home interface values from Luxtronik controller.",
        LUXTRONIK_DEFAULT_MODBUS_PORT
    )
    args = parser.parse_args()
    print(f"Dump SHI of {args.ip}:{args.port}")

    shi = create_modbus_tcp(args.ip, args.port)

    dump_fields(shi.read_inputs)
    dump_fields(shi.read_holdings)


if __name__ == "__main__":
    dump_shi()
