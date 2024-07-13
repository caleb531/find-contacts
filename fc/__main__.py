#!/usr/bin/env python3

# The CLI for the Find Contacts program

import argparse
import json

import fc.core as core


def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("search_query")
    return parser.parse_args()


def main() -> None:

    cli_args = get_cli_args()
    for result in core.find_contacts(cli_args.search_query):
        print(json.dumps(result, indent=2, separators=(",", ": ")))


if __name__ == "__main__":
    main()
