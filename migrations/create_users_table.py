import base64
import json
import os

from whoami import auth, config, db


def headshot() -> str:
    with open(
        os.path.join(config.WHOAMI_DIR, config.WHOAMI_ASSETS_DIR, "whoami_headshot.svg"),
        "rb",
    ) as f:
        svg = f.read()

    svg_encoded = base64.b64encode(svg).decode("UTF-8")
    return svg_encoded


def up() -> None:
    sql = db.connection()
    cur = sql.cursor()
    cur.executescript(
        """
        CREATE TABLE migration_versions(
            version TEXT PRIMARY KEY
        );
        CREATE TABLE users(
            username TEXT PRIMARY KEY NOT NULL,
            about BLOB NOT NULL,
            headshot TEXT NOT NULL,
            hashed_password TEXT NOT NULL
        );
        """
    )
    sql.commit()
    hashed_password = auth.get_password_hash(config.WHOAMI_PASSWORD)
    cur.execute(
        """
        INSERT INTO users(username, about, headshot, hashed_password) VALUES(?, ?, ?, ?)""",
        (
            config.WHOAMI_USERNAME,
            json.dumps({}),
            headshot(),
            hashed_password,
        ),
    )
    cur.execute("INSERT INTO migration_versions VALUES(?)", ("create_users_table",))
    sql.commit()
    cur.execute("VACUUM")
    sql.commit()
    sql.close()


def down() -> None:
    sql = db.connection()
    cur = sql.cursor()
    cur.execute("DROP TABLE users;")
    cur.execute("DROP TABLE migration_versions;")
    sql.commit()
    cur.execute("VACUUM")
    sql.commit()
    sql.close()
