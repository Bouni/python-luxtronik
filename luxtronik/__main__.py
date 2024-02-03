"""Luxtronik CLI."""

import argparse
import sys
from luxtronik.discover import discover as _discover
from luxtronik.scripts.dump_luxtronik import (
    dump_luxtronik,
)  # pylint: disable=unused-import # noqa: F401
from luxtronik.scripts.dump_changes import (
    dump_changes,
)  # pylint: disable=unused-import # noqa: F401


def discover():
    """Output available heat pump controllers nicely."""
    results = _discover()
    print(f"{len(results)} heatpump(s) reported back")
    for count, result in enumerate(results):
        print(f"Heat pump #{count} -> IP address: {result[0]} port: {result[1]}")


def main() -> int:
    """Entry point to parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="CLI for Luxtronik controllers",
        usage="""luxtronik <command> [<args>]
        The supported commands are:
        dump       Dump all available data from the Luxtronik controller 
        changes    Dump all value changes from Luxtronik controller  
        discover   Discover Luxtronik controllers on the network (via magic packet) and output results
        """,
    )
    parser.add_argument("command", help="Subcommand to run")
    # parse_args defaults to [1:] for args, but you need to
    # exclude the rest of the args too, or validation will fail
    args = parser.parse_args(sys.argv[1:2])
    commands = {
        "dump": dump_luxtronik,
        "changes": dump_changes,
        "discover": discover,
    }
    if args.command not in commands:
        print("Unrecognized command")
        parser.print_help()
        sys.exit(1)
    # pop command, otherwise the argparser within the called script will fail
    sys.argv.pop(1)
    # call the corresponding command
    commands[args.command]()
