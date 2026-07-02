#! /usr/bin/env python3

# pylint: disable=invalid-name
"""
Script to debug the config interface of a Luxtronik controller
"""
import logging

from luxtronik import LuxtronikSocketInterface, LUXTRONIK_DEFAULT_PORT
from luxtronik.scripts import create_default_args_parser, get_port_from_ip_string

logging.basicConfig(level=logging.DEBUG)

SUPPORTED_CMDS = ["write-param", "read-param", "read-calc", "read-visi"]


def try_text_to_number(text):
    value = text
    try:
        value = float(value)
    except ValueError:
        pass
    try:
        value = int(value)
    except ValueError:
        pass
    return value

def debug_cfi():
    parser = create_default_args_parser(
        "Debug commands for the config interface of a Luxtronik controller",
        LUXTRONIK_DEFAULT_PORT,
        False
    )
    parser.add_argument("cmd", type=str, help="Command to execute. Currently supported: {SUPPORTED_CMDS}.")
    parser.add_argument("target", help="The target to be read or written. May be a index or name.")
    parser.add_argument("value", nargs="?", default=None, help="Value to be written")
    args = parser.parse_args()
    port = get_port_from_ip_string(args, LUXTRONIK_DEFAULT_PORT)

    client = LuxtronikSocketInterface(args.ip, port)

    if args.cmd == SUPPORTED_CMDS[0]:
        print(f"Write {args.value} to CFI parameter {args.target} of {args.ip}:{port}")
        value = try_text_to_number(args.value)
        client.write_parameter(args.target, value)

    elif args.cmd == SUPPORTED_CMDS[1]:
        print(f"Read parameter from CFI {args.target} of {args.ip}:{port}")
        parameters = client.read_parameters()
        field = parameters[args.target]
        print(f"{repr(field)}")

    elif args.cmd == SUPPORTED_CMDS[2]:
        print(f"Read calculation from CFI {args.target} of {args.ip}:{port}")
        calculations = client.read_calculations()
        field = calculations[args.target]
        print(f"{repr(field)}")

    elif args.cmd == SUPPORTED_CMDS[3]:
        print(f"Read visibilities from CFI {args.target} of {args.ip}:{port}")
        visibilities = client.read_visibilities()
        field = visibilities[args.target]
        print(f"{repr(field)}")

    else:
        print(f"Cmd '{args.cmd}' not supported. Use on of {SUPPORTED_CMDS}")


if __name__ == "__main__":
    debug_cfi()
