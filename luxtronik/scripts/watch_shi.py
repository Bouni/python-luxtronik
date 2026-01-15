#! /usr/bin/env python3

# pylint: disable=invalid-name
"""
Script to watch all smart home interface value changes of the Luxtronik controller
"""

from collections import OrderedDict
import logging

from luxtronik.shi import create_modbus_tcp, LUXTRONIK_DEFAULT_MODBUS_PORT
from luxtronik.scripts.update_screen import UpdateScreen
from luxtronik.scripts import (
    create_default_args_parser,
    print_watch_header,
    update_changes
)

logging.disable(logging.CRITICAL)


def dump_all(screen, client, changes, prev_data, this_data):
    # Get new data
    client.read(this_data)

    # Compare this values with the initial values
    # and add changes to dictionary
    update_changes(changes, prev_data.inputs, this_data.inputs)
    update_changes(changes, prev_data.holdings, this_data.holdings)

    # Print changes
    print_watch_header(screen, f"Watch SHI of {client._interface._client._host}:{client._interface._client._port}")
    sorted_changes = OrderedDict(sorted(changes.items()))
    for key, values in sorted_changes.items():
        screen.write(values)

def dump_repeated(client):
    prev_data = client.read()
    this_data = client.create_data()
    changes = {}
    screen = UpdateScreen(500)

    screen.clear()
    while True:
        dump_all(screen, client, changes, prev_data, this_data)
        screen.update()
        if screen.process_keys(100):
            break
        screen.reset()

def watch_shi():
    parser = create_default_args_parser(
        "Watch all smart home interface value changes of the Luxtronik controller",
        LUXTRONIK_DEFAULT_MODBUS_PORT
    )
    args = parser.parse_args()
    client = create_modbus_tcp(args.ip, args.port)
    dump_repeated(client)


if __name__ == "__main__":
    watch_shi()
