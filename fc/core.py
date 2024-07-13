#!/usr/bin/env python3

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
    sql_path = importlib.resources.files(__package__).joinpath(
        os.path.join("queries", "find_contacts.sql")
    )
    with open(str(sql_path), "r") as sql_file:
        return sql_file.read()


def prettify_column_name(column_name: str) -> str:
    # Strip 'Z' prefix and convert to lowercase
    return column_name[1:].lower()


def convert_row_to_dict(*args: Any, **kwargs: Any) -> dict:
    return dict(sqlite3.Row(*args, **kwargs))


def find_contacts_in_db(
    sql_db_path: str, search_query: str
) -> Generator[dict, None, None]:
    with sqlite3.connect(sql_db_path) as con:
        # <https://stackoverflow.com/a/3300514/560642>
        con.row_factory = convert_row_to_dict
        cur = con.cursor()
        rows: list[dict] = cur.execute(
            get_sql_query(), {"search_query_like": f"{search_query}%"}
        ).fetchall()
        return (
            {
                **{
                    prettify_column_name(key): value for key, value in dict(row).items()
                },
                "sourceid": os.path.expanduser(
                    os.path.join(
                        "~",
                        "Library",
                        "Application Support",
                        "AddressBook",
                        "Sources",
                        os.path.basename(os.path.dirname(sql_db_path)),
                        "Metadata",
                        f'{dict(row)["ZUNIQUEID"]}.abcdp',
                    )
                ),
            }
            for row in rows
        )


def find_contacts(search_query: str) -> list[dict]:
    results: list[dict] = []
    for sql_db_path in glob.iglob(SQL_DB_GLOB):
        results.extend(find_contacts_in_db(sql_db_path, search_query))
    return results
