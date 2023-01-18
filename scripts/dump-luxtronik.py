#! /usr/bin/env python3

from luxtronik import Luxtronik

l = Luxtronik('192.168.88.11', 8889)

print("="*80)
print ('{:^80}'.format(' Parameters '))
print("="*80)

for n, p in l.parameters.parameters.items():
    print(f"Number: {n:<5} Name: {p.name:<60} Type: {p.__class__.__name__:<20} Value: {p.value}")

print("="*80)
print ('{:^80}'.format(' Calculations '))
print("="*80)

for n, c in l.calculations.calculations.items():
    print(f"Number: {n:<5} Name: {c.name:<60} Type: {c.__class__.__name__:<20} Value: {c.value}")

print("="*80)
print ('{:^80}'.format(' Visibilities '))
print("="*80)

for n, v in l.visibilities.visibilities.items():
    print(f"Number: {n:<5} Name: {v.name:<60} Type: {v.__class__.__name__:<20} Value: {v.value}")
