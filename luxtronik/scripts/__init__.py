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

def dump_fields(data_vector):
    print_dump_header(f"{data_vector.name}s")
    for index, field in data_vector.data.items():
        print_dump_row(index, field)

def print_watch_header(screen, caption):
    cols, _ = screen.get_visible_size()
    screen.write("=" * cols)
    screen.write(caption)
    screen.write("=" * cols)

def get_watch_row(short_name, number, prev_field, this_field):
    text = f"{short_name}: Number: {number:<5} Name: {prev_field.name:<60} " + f"Value: {prev_field}"
    if this_field:
        text += f" -> {this_field}"
    return text

def update_changes(changes, prev_data_vector, this_data_vector):
    for index, this_field in this_data_vector.data.items():
        short_name = this_data_vector.name[:4]
        key = f"{short_name}_{str(index).zfill(5)}"
        prev_field = prev_data_vector.get(index)
        if this_field.raw != prev_field.raw:
            changes[key] = get_watch_row(short_name, index, prev_field, this_field)
        elif key in changes:
            changes[key] = get_watch_row(short_name, index, prev_field, None)
