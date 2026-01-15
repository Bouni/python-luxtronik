#! /usr/bin/env python3

# pylint: disable=invalid-name
"""
Script to dump all available config interface values of the Luxtronik controller
"""

from luxtronik import Luxtronik, LUXTRONIK_DEFAULT_PORT
from luxtronik.scripts import create_default_args_parser, dump_fields


def dump_all(client):
    dump_fields(client.parameters)
    dump_fields(client.calculations)
    dump_fields(client.visibilities)

def dump_cfi():
    parser = create_default_args_parser(
        "Dumps all config interface values of the Luxtronik controller",
        LUXTRONIK_DEFAULT_PORT
    )
    args = parser.parse_args()
    print(f"Dump CFI of {args.ip}:{args.port}")
    client = Luxtronik(args.ip, args.port)
    dump_all(client)


if __name__ == "__main__":
    dump_cfi()
