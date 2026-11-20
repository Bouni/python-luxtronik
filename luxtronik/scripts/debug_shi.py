#! /usr/bin/env python3

# pylint: disable=invalid-name
"""
Script to debug the smart-home interface of a Luxtronik controller
"""
import logging

from luxtronik.shi import create_modbus_tcp, LUXTRONIK_DEFAULT_MODBUS_PORT
from luxtronik.scripts import create_default_args_parser, get_port_from_ip_string

logging.basicConfig(level=logging.DEBUG)

SUPPORTED_CMDS = ["write-holding", "read-holding", "read-input"]


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

def debug_shi():
    parser = create_default_args_parser(
        "Debug commands for the smart-home interface of a Luxtronik controller",
        LUXTRONIK_DEFAULT_MODBUS_PORT,
        False
    )
    parser.add_argument("cmd", type=str, help="Command to execute. Currently supported: {SUPPORTED_CMDS}.")
    parser.add_argument("target", help="The target to be read or written. May be a index or name.")
    parser.add_argument("value", nargs="?", default=None, help="Value to be written")
    args = parser.parse_args()
    port = get_port_from_ip_string(args, LUXTRONIK_DEFAULT_MODBUS_PORT)

    client = create_modbus_tcp(args.ip, port)

    if args.cmd == SUPPORTED_CMDS[0]:
        print(f"Write {args.value} to SHI holding {args.target} of {args.ip}:{port}")
        value = try_text_to_number(args.value)
        client.write_holding(args.target, value)

    elif args.cmd == SUPPORTED_CMDS[1]:
        print(f"Read holding from SHI {args.target} of {args.ip}:{port}")
        holding = client.read_holding(args.target)
        print(f"{repr(holding)}")

    elif args.cmd == SUPPORTED_CMDS[2]:
        print(f"Read input from SHI {args.target} of {args.ip}:{port}")
        input = client.read_input(args.target)
        print(f"{repr(input)}")

    else:
        print(f"Cmd '{args.cmd}' not supported. Use on of {SUPPORTED_CMDS}")


if __name__ == "__main__":
    debug_shi()
