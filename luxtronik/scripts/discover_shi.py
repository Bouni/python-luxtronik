#! /usr/bin/env python3
# pylint: disable=invalid-name
"""
Script to scan all inputs/holdings of the smart home interface.
Only undefined but existing fields will be dumped.
"""

import logging

from luxtronik.scripts import (
    create_default_args_parser,
    print_dump_header,
    print_dump_row
)
from luxtronik.datatypes import Unknown
from luxtronik.shi.constants import LUXTRONIK_DEFAULT_MODBUS_PORT
from luxtronik.shi.modbus import LuxtronikModbusTcpInterface
from luxtronik.shi.inputs import INPUTS_DEFINITIONS
from luxtronik.shi.holdings import HOLDINGS_DEFINITIONS

logging.disable(logging.CRITICAL)

def get_undefined(definitions, start, count):
    skip_count = 0
    undefined = []
    for i in range(start, start + count):
        # Skip addresses that belongs to a previous field
        if skip_count > 0:
            skip_count -= 1
            continue
        definition = definitions[i]
        # Add unknown
        if definition is None:
            undefined.append((i, None, Unknown(f"unknown_{definitions.name}_{i}", False)))
        else:
            skip_count = definition.count - 1
    return undefined

def get_defined(definitions):
    defined = []
    for definition in definitions:
        defined.append((definition.index, definition, definition.create_field()))
    return defined

def dump_undefined(undefined, offset, read_cb):
    for number, _, field in undefined:
        print(f"Number: {number:<5}", end="\r")
        data = read_cb(number + offset, 1)
        if data is not None:
            field.raw = data[0]
            print_dump_row(number, field)

def dump_defined(defined, offset, read_cb):
    for number, definition, field in defined:
        print(f"Number: {number:<5}", end="\r")
        data = read_cb(number + offset, definition.count)
        if data is None:
            field.raw = None
            print_dump_row(number, field)

def discover_fields(definitions, start, count, read_cb):
    print_dump_header(f"Undefined but existing {definitions.name}s")
    undefined = get_undefined(definitions, start, count)
    dump_undefined(undefined, definitions.offset, read_cb)

def discontinue_fields(definitions, read_cb):
    print_dump_header(f"Defined but not existing {definitions.name}s")
    defined = get_defined(definitions)
    dump_defined(defined, definitions.offset, read_cb)

def discover_shi():
    parser = create_default_args_parser(
        "Dumps all undefined but existing fields of the smart home interface.",
        LUXTRONIK_DEFAULT_MODBUS_PORT
    )
    parser.add_argument(
        "count",
        nargs="?",
        type=int,
        default=1000,
        help="Total number of registers to check",
    )
    args = parser.parse_args()
    print(f"Discover SHI of {args.ip}:{args.port}")

    client = LuxtronikModbusTcpInterface(args.ip, args.port)

    discover_fields(INPUTS_DEFINITIONS, 0, args.count, client.read_inputs)
    discontinue_fields(INPUTS_DEFINITIONS, client.read_inputs)
    discover_fields(HOLDINGS_DEFINITIONS, 0, args.count, client.read_holdings)
    discontinue_fields(HOLDINGS_DEFINITIONS, client.read_holdings)

    # Clear last line if nothing was found
    print(' '*100)


if __name__ == "__main__":
    discover_shi()
