#! /usr/bin/env python3

# pylint: disable=invalid-name

"""Script to dump all available values from Luxtronik controller"""
import argparse

from luxtronik import Luxtronik
from luxtronik.constants import LUXTRONIK_DEFAULT_PORT


def dump_luxtronik():
    # pylint: disable=duplicate-code
    """Dump all available data from the Luxtronik controller."""
    parser = argparse.ArgumentParser(description="Dumps all values from Luxtronik controller")
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
    # pylint: enable=duplicate-code

    print("=" * 80)
    print(f"{' Parameter ': ^80}")
    print("=" * 80)

    for number, param in client.parameters:
        print(f"Number: {number:<5} Name: {param.name:<60} " + f"Type: {param.__class__.__name__:<20} Value: {param}")

    print("=" * 80)
    print(f"{' Calculations ': ^80}")
    print("=" * 80)

    for number, calc in client.calculations:
        print(f"Number: {number:<5} Name: {calc.name:<60} " + f"Type: {calc.__class__.__name__:<20} Value: {calc}")

    print("=" * 80)
    print(f"{' Visibilities ': ^80}")
    print("=" * 80)

    for number, visi in client.visibilities:
        print(f"Number: {number:<5} Name: {visi.name:<60} " + f"Type: {visi.__class__.__name__:<20} Value: {visi}")


if __name__ == "__main__":
    dump_luxtronik()
