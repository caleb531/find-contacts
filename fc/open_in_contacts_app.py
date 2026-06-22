#!/usr/bin/env python3

# The Alfred action for opening contacts in the Contacts app

import subprocess
import sys
from pathlib import Path

CONTACT_ID_SUFFIX = ":ABPerson"


def get_contact_id(path: str) -> str:
    # Contacts metadata filenames normally carry the AddressBook record id
    # The URL scheme needs the ABPerson suffix even when the file stem omits it
    contact_id = Path(path).with_suffix("").name
    if not contact_id.endswith(CONTACT_ID_SUFFIX):
        contact_id = f"{contact_id}{CONTACT_ID_SUFFIX}"
    return contact_id


def open_contact(contact_id: str) -> None:
    # Delegate to macOS so the Contacts app handles the custom addressbook URL
    subprocess.run(["open", f"addressbook://{contact_id}"], check=True)


def main(paths: list[str]) -> None:
    for path in paths:
        open_contact(get_contact_id(path))


if __name__ == "__main__":
    main(sys.argv[1:])
