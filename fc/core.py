#!/usr/bin/env python3

# The core library of functions for finding contacts

import functools
import glob
import importlib.resources
import os
import os.path
import sqlite3
from typing import Any, Generator

SQL_DB_GLOB = os.path.expanduser(
    os.path.join(
        "~",
        "Library",
        "Application Support",
        "AddressBook",
        "Sources",
        "*",
        "AddressBook-v*.abcddb",
    )
)


@functools.lru_cache()
def get_sql_query() -> str:
    sql_path = importlib.resources.files("fc").joinpath(
        os.path.join("queries", "find_contacts.sql")
    )
    with open(str(sql_path), "r") as sql_file:
        return sql_file.read()


def prettify_column_name(column_name: str) -> str:
    # Strip 'Z' prefix and convert to lowercase
    return column_name[1:].lower()


def convert_row_to_dict(*args: Any, **kwargs: Any) -> dict:
    return dict(sqlite3.Row(*args, **kwargs))


# The search query is already sanitized for SQL syntax when passed to the
# execute() call as a parameter, but we stil need to escape LIKE clause special
# characters ('%' and '_')
def escape_search_query(search_query: str) -> str:
    return search_query.replace("%", "\\%").replace("_", "\\_")


def find_contacts_in_db(
    sql_db_path: str, search_query: str
) -> Generator[dict, None, None]:
    with sqlite3.connect(sql_db_path) as con:
        # <https://stackoverflow.com/a/3300514/560642>
        con.row_factory = convert_row_to_dict
        cur = con.cursor()
        rows: list[dict] = cur.execute(
            get_sql_query(),
            {"search_query_like": f"{escape_search_query(search_query)}%"},
        ).fetchall()
        return (
            {
                **{
                    prettify_column_name(key): value for key, value in dict(row).items()
                },
                "filepath": os.path.expanduser(
                    os.path.join(
                        "~",
                        "Library",
                        "Application Support",
                        "AddressBook",
                        "Sources",
                        os.path.basename(os.path.dirname(sql_db_path)),
                        "Metadata",
                        f"{dict(row)['ZUNIQUEID']}.abcdp",
                    )
                ),
            }
            for row in rows
        )


def find_contacts(search_query: str) -> list[dict]:
    contacts: list[dict] = []
    for sql_db_path in glob.iglob(SQL_DB_GLOB):
        contacts.extend(find_contacts_in_db(sql_db_path, search_query))
    return contacts
