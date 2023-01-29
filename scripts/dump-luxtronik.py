#! /usr/bin/env python3

# pylint: disable=invalid-name

"""Script to dump all values from Luxtronik controller"""

import argparse

from luxtronik import Luxtronik

parser = argparse.ArgumentParser(
        description="Dumps all values from Luxtronik controller"
    )
parser.add_argument(
        "ip",
        help="IP address of Luxtronik controller to connect to"
    )
parser.add_argument(
        "port",
        nargs="?",
        type=int,
        default=8889,
        help="Port to use to connect to Luxtronik controller"
    )
args = parser.parse_args()

client = Luxtronik(args.ip, args.port)

print("="*80)
print(f"{' Parameter ': ^80}")
print("="*80)

for number, param in client.parameters.parameters.items():
    print(f"Number: {number:<5} Name: {param.name:<60} Type: {param.__class__.__name__:<20} Value: {param.value}")

print("="*80)
print(f"{' Calculations ': ^80}")
print("="*80)

for number, calc in client.calculations.calculations.items():
    print(f"Number: {number:<5} Name: {calc.name:<60} Type: {calc.__class__.__name__:<20} Value: {calc.value}")

print("="*80)
print(f"{' Visibilities ': ^80}")
print("="*80)

for number, visi in client.visibilities.visibilities.items():
    print(f"Number: {number:<5} Name: {visi.name:<60} Type: {visi.__class__.__name__:<20} Value: {visi.value}")
