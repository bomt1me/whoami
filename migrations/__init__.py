import sqlite3

from whoami import db

from migrations import (
    create_users_table,
    create_blogs_table,
)


MAP_UP = {None: create_users_table, "create_users_table": create_blogs_table}

MAP_DOWN = {
    "create_users_table": create_users_table,
    "create_blogs_table": create_blogs_table,
}


def up():
    try:
        version = db.MigrationVersion.get()
    except sqlite3.OperationalError:
        version = None

    caller = MAP_UP.get(version)
    if caller is None:
        return

    caller.up()


def down():
    try:
        version = db.MigrationVersion.get()
    except sqlite3.OperationalError:
        version = None

    caller = MAP_DOWN.get(version)
    if caller is None:
        return

    caller.down()
