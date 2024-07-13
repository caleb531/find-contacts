#!/usr/bin/env python3

# The script filter for the Alfred Workflow

import json
import sys

import fc.core as core


def get_contact_display_name(contact: dict) -> str:
    if contact["firstname"] and contact["lastname"]:
        return f"{contact['firstname']} {contact['lastname']}"
    if contact["firstname"]:
        return contact["firstname"]
    if contact["nickname"]:
        return contact["nickname"]
    elif contact["organization"]:
        return contact["organization"]
    else:
        return ""


def get_result(contact: dict) -> dict:
    return {
        "type": "file",
        "uid": contact["filepath"],
        "arg": contact["filepath"],
        "title": get_contact_display_name(contact),
        "subtitle": "View in Alfred",
    }


def get_result_list(search_query: str) -> list[dict]:
    return [get_result(contact) for contact in core.find_contacts(search_query)]


def main(query_str: str) -> None:

    results = get_result_list(query_str)
    if not results:
        results.append(
            {
                "title": "No Results",
                "subtitle": "No contacts matching '{}'".format(query_str),
                "valid": False,
            }
        )

    print(json.dumps({"items": results}))


if __name__ == "__main__":
    main(sys.argv[1])
