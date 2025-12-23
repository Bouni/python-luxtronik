#! /usr/bin/env python3
# pylint: disable=invalid-name, disable=too-many-locals
"""
Script to watch all value changes from the Smart-Home-Interface of the Luxtronik controller
"""

from collections import OrderedDict
import logging
#import select
#import sys
import time

from luxtronik.scripts import (
    create_default_args_parser,
    print_watch_header
)
from luxtronik.shi import create_modbus_tcp
from luxtronik.shi.constants import LUXTRONIK_DEFAULT_MODBUS_PORT

logging.disable(logging.CRITICAL)

def update_changes(changes, this_data_vector, prev_data_vector):
    for definition, this_field in this_data_vector.items():
        short_name = this_data_vector.name[:4]
        number = definition.index
        key = f"{short_name}_{str(number).zfill(5)}"
        prev_field = prev_data_vector.get(number)
        if this_field.raw != prev_field.raw:
            changes[key] = (
                f"{short_name}: Number: {number:<5} Name: {prev_field.name:<60} " + f"Value: {prev_field} -> {this_field}"
            )
        elif key in changes:
            changes[key] = (
                f"{short_name}: Number: {number:<5} Name: {prev_field.name:<60} " + f"Value: {prev_field}"
            )

def watch_shi():
    parser = create_default_args_parser(
        "Watch all value changes from the Smart-Home-Interface of the Luxtronik controller.",
        LUXTRONIK_DEFAULT_MODBUS_PORT
    )
    args = parser.parse_args()

    shi = create_modbus_tcp(args.ip, args.port)

    prev_data = shi.read()
    this_data = shi.create_data()
    changes = {}

    print("\033[2J") # clear screen

    while True:
        # Get new data
        shi.read(this_data)

        # Compare this values with the initial values
        # and add changes to dictionary
        update_changes(changes, this_data.inputs, prev_data.inputs)
        update_changes(changes, this_data.holdings, prev_data.holdings)

        # Print changes
        print("\033[H") # Go-to home, line 0
        #print_watch_header(f"Watch SHI of {args.ip}:{args.port}: Press a key and enter to: q = quit; r = reset")
        print_watch_header(f"Watch SHI of {args.ip}:{args.port}")
        sorted_changes = OrderedDict(sorted(changes.items()))
        for key, values in sorted_changes.items():
            print(values + "\033[0K") # clear residual line
        print("\n")

        # Read stdin
        # input, _, _ = select.select([sys.stdin], [], [], 0.1)
        # if input:
        #     key = sys.stdin.read(1)
        #     if key == 'q':
        #         break
        #     elif key == 'r':
        #         prev_data = client.read()
        #         changes = {}
        #         print("\033[2J") # clear screen

        time.sleep(1)


if __name__ == "__main__":
    watch_shi()
