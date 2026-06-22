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
    result_list = core.find_contacts(cli_args.search_query.strip())

    # Emit one formatted JSON object per contact so the CLI stays easy to pipe
    # into tools while still being readable during manual debugging
    for result in result_list:
        print(json.dumps(result, indent=2, separators=(",", ": ")))


if __name__ == "__main__":
    main()
