import json

from whoami import auth, config, db


def up() -> None:
    sql = db.connection()
    cur = sql.cursor()
    cur.execute(
        """
        CREATE TABLE blogs(
            id INTEGER PRIMARY KEY NOT NULL,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            tags TEXT NOT NULL,
            content BLOB NOT NULL,
            state INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        );
        """
    )
    cur.execute("UPDATE migration_versions SET version = ?;", ("create_blogs_table",))
    sql.commit()
    cur.execute("VACUUM")
    sql.commit()
    sql.close()


def down() -> None:
    sql = db.connection()
    cur = sql.cursor()
    cur.execute("DROP TABLE blogs;")
    cur.execute("UPDATE migration_versions SET version = ?;", ("create_users_table",))
    sql.commit()
    cur.execute("VACUUM")
    sql.commit()
    sql.close()
