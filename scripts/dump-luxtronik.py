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

l = Luxtronik(args.ip, args.port)

print("="*80)
print(f"{' Parameter ': ^80}")
print("="*80)

for n, p in l.parameters.parameters.items():
    print(f"Number: {n:<5} Name: {p.name:<60} Type: {p.__class__.__name__:<20} Value: {p.value}")

print("="*80)
print(f"{' Calculations ': ^80}")
print("="*80)

for n, c in l.calculations.calculations.items():
    print(f"Number: {n:<5} Name: {c.name:<60} Type: {c.__class__.__name__:<20} Value: {c.value}")

print("="*80)
print(f"{' Visibilities ': ^80}")
print("="*80)

for n, v in l.visibilities.visibilities.items():
    print(f"Number: {n:<5} Name: {v.name:<60} Type: {v.__class__.__name__:<20} Value: {v.value}")
