#! /usr/bin/env python3

# pylint: disable=invalid-name
"""
Script to dump all available smart home interface values of the Luxtronik controller
"""

import logging

from luxtronik.shi import create_modbus_tcp, LUXTRONIK_DEFAULT_MODBUS_PORT
from luxtronik.scripts import create_default_args_parser, dump_fields

logging.disable(logging.CRITICAL)


def dump_all(client):
    dump_fields(client.read_inputs())
    dump_fields(client.read_holdings())

def dump_shi():
    parser = create_default_args_parser(
        "Dumps all smart home interface values of the Luxtronik controller",
        LUXTRONIK_DEFAULT_MODBUS_PORT
    )
    args = parser.parse_args()
    print(f"Dump SHI of {args.ip}:{args.port}")
    client = create_modbus_tcp(args.ip, args.port)
    dump_all(client)


if __name__ == "__main__":
    dump_shi()
