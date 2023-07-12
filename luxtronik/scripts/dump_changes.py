#! /usr/bin/env python3

# pylint: disable=invalid-name, disable=too-many-locals

"""Script to dump all value changes from Luxtronik controller"""

import os
import time
import argparse

from luxtronik import Luxtronik
from luxtronik.constants import LUXTRONIK_DEFAULT_PORT


def dump_changes():
    """Dump all value changes from Luxtronik controller"""
    # pylint: disable=duplicate-code
    parser = argparse.ArgumentParser(
        description="Dumps all value changes from Luxtronik controller"
    )
    parser.add_argument("ip", help="IP address of Luxtronik controller to connect to")
    parser.add_argument(
        "port",
        nargs="?",
        type=int,
        default=LUXTRONIK_DEFAULT_PORT,
        help="Port to use to connect to Luxtronik controller",
    )
    args = parser.parse_args()

    client = Luxtronik(args.ip, args.port)
    prev_calcs, prev_params, prev_visis = client.read()
    # pylint: enable=duplicate-code
    changes = {}

    while True:
        # Get new data
        this_calcs, this_params, this_visis = client.read()

        # Compare this values with the initial values
        # and add changes to dictionary
        for number, param in this_params:
            key = f"para_{number}"
            prev_param = prev_params.get(number)
            if param.raw != prev_param.raw:
                changes[key] = (
                    f"para: Number: {number:<5} Name: {prev_param.name:<60} "
                    + f"Value: {prev_param} -> {param}"
                )
            elif key in changes:
                changes[key] = (
                    f"para: Number: {number:<5} Name: {prev_param.name:<60} "
                    + f"Value: {prev_param} -> reverted"
                )

        for number, calc in this_calcs:
            key = f"calc_{number}"
            prev_calc = prev_calcs.get(number)
            if calc.raw != prev_calc.raw:
                changes[key] = (
                    f"calc: Number: {number:<5} Name: {prev_calc.name:<60} "
                    + f"Value: {prev_calc} -> {calc}"
                )
            elif key in changes:
                changes[key] = (
                    f"calc: Number: {number:<5} Name: {prev_calc.name:<60} "
                    + f"Value: {prev_calc} -> reverted"
                )

        for number, visi in this_visis:
            key = f"visi_{number}"
            prev_visi = prev_visis.get(number)
            if visi.raw != prev_visi.raw:
                changes[key] = (
                    f"visi: Number: {number:<5} Name: {prev_visi.name:<60} "
                    + f"Value: {prev_visi} -> {visi}"
                )
            elif key in changes:
                changes[key] = (
                    f"visi: Number: {number:<5} Name: {prev_visi.name:<60} "
                    + f"Value: {prev_visi} -> reverted"
                )

        # Print changes
        os.system("clear")
        print("=" * 80)
        for key, values in changes.items():
            print(values)
        time.sleep(1)


if __name__ == "__main__":
    dump_changes()
