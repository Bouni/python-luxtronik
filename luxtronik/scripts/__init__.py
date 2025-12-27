"""Luxtronik script helper."""

import argparse

def create_default_args_parser(func_desc, default_port):
    parser = argparse.ArgumentParser(description=func_desc)
    parser.add_argument("ip", help="IP address of Luxtronik controller to connect to")
    parser.add_argument(
        "port",
        nargs="?",
        type=int,
        default=default_port,
        help="Port to use to connect to Luxtronik controller",
    )
    return parser

def print_dump_header(caption):
    print("=" * 130)
    print(f"{' ' + caption + ' ': ^120}")
    print("=" * 130)

def print_dump_row(number, field):
    print(f"Number: {number:<5} Name: {field.name:<60} " + f"Type: {field.__class__.__name__:<20} Value: {field}")

def print_watch_header(caption):
    print("=" * 130)
    print(caption)
    print("=" * 130)
