#!/usr/bin/env python3

# The script filter for the Alfred Workflow
import json
import os
import os.path
import sys
from pathlib import Path

import fc.core as core


def get_contact_display_name(contact: dict) -> str:
    # Prefer human names, then fall back to the fields that Contacts uses for
    # people or organization-only records
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


# Upgrading macOS Tahoe 26.4 seemingly removes the *.abcdp files, but if we
# recreate empty stub files with the same filenames, then it somehow restores
# Alfred's ability to preview the contact
def create_metadata_stub(contact_filepath: str) -> None:
    os.makedirs(os.path.dirname(contact_filepath), exist_ok=True)
    Path(contact_filepath).touch(exist_ok=True)


def get_result(contact: dict) -> dict:
    create_metadata_stub(contact["filepath"])

    # Alfred expects Script Filter results in this shape
    # Using the metadata file as both uid and arg lets the next workflow action
    # open the contact
    return {
        "uid": contact["filepath"],
        "arg": contact["filepath"],
        "title": get_contact_display_name(contact),
        "subtitle": "View in Alfred",
        "icon": {
            "type": "fileicon",
            "path": contact["filepath"],
        },
    }


def get_result_list(search_query: str) -> list[dict]:
    return [get_result(contact) for contact in core.find_contacts(search_query)]


def main(query_str: str) -> None:
    query_str = query_str.strip()
    results = get_result_list(query_str)
    if not results:
        # Returning a disabled item gives Alfred an explicit empty state instead
        # of rendering a blank result list
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
