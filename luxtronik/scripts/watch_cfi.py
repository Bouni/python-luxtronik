#! /usr/bin/env python3

# pylint: disable=invalid-name
"""
Script to watch all config interface value changes of the Luxtronik controller
"""

from collections import OrderedDict

from luxtronik import LuxtronikSocketInterface, LuxtronikData, LUXTRONIK_DEFAULT_PORT
from luxtronik.scripts.update_screen import UpdateScreen
from luxtronik.scripts import (
    create_default_args_parser,
    print_watch_header,
    update_changes
)


def dump_all(screen, client, changes, prev_data, this_data):
    # Get new data
    client.read(this_data)

    # Compare this values with the initial values
    # and add changes to dictionary
    update_changes(changes, prev_data.parameters, this_data.parameters)
    update_changes(changes, prev_data.calculations, this_data.calculations)
    update_changes(changes, prev_data.visibilities, this_data.visibilities)

    # Print changes
    print_watch_header(screen, f"Watch CFI of {client._host}:{client._port}")
    sorted_changes = OrderedDict(sorted(changes.items()))
    for key, values in sorted_changes.items():
        screen.write(values)

def dump_repeated(client):
    prev_data = client.read()
    this_data = LuxtronikData()
    changes = {}
    screen = UpdateScreen(500)

    screen.clear()
    while True:
        dump_all(screen, client, changes, prev_data, this_data)
        screen.update()
        if screen.process_keys(100):
            break
        screen.reset()

def watch_cfi():
    parser = create_default_args_parser(
        "Watch all config interface value changes of the Luxtronik controller",
        LUXTRONIK_DEFAULT_PORT
    )
    args = parser.parse_args()
    client = LuxtronikSocketInterface(args.ip, args.port)
    dump_repeated(client)


if __name__ == "__main__":
    watch_cfi()
