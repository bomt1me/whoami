from typing import Any, Dict, List, Optional

import datetime
import enum
import json
import os
import sqlite3

from whoami import config


class BlogState(enum.Enum):
    ACTIVE = 0
    DELETED = 1


def connection() -> sqlite3.Connection:
    return sqlite3.connect(os.path.join(config.WHOAMI_DIR, config.WHOAMI_DB_NAME))


class UserDto:
    def __init__(self, *, first_name: str, last_name: str, **kwargs) -> None:
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            sorted(
                {
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                }.items()
            )
        )


class User:
    @classmethod
    def get_hashed_password(cls, username: str) -> Optional[str]:
        sql = connection()
        cur = sql.cursor()
        res_hashed_password = cur.execute(
            "SELECT hashed_password FROM users WHERE username = ?;", (username,)
        )
        hashed_password = res_hashed_password.fetchone()
        sql.close()
        if hashed_password:
            return hashed_password[0]

        return None

    @classmethod
    def update(cls, username: str, user: UserDto) -> None:
        about = json.dumps(user.to_dict())
        sql = connection()
        cur = sql.cursor()
        cur.execute(
            "UPDATE users SET about = ? WHERE username = ?",
            (
                about,
                username,
            ),
        )
        sql.commit()
        sql.close()

    @classmethod
    def update_headshot(cls, username: str, headshot: str) -> None:
        sql = connection()
        cur = sql.cursor()
        cur.execute(
            "UPDATE users SET headshot = ? WHERE username = ?",
            (
                headshot,
                username,
            ),
        )
        sql.commit()
        sql.close()

    @classmethod
    def get(cls, username: str) -> Optional[UserDto]:
        sql = connection()
        cur = sql.cursor()
        res_user = cur.execute("SELECT about FROM users WHERE username = ?", (username,)).fetchone()
        sql.commit()
        sql.close()
        if res_user:
            loaded_user = json.loads(res_user[0])
            if loaded_user:
                return UserDto(**loaded_user)

            return None

        return None

    @classmethod
    def get_headshot(cls, username: str) -> Optional[str]:
        sql = connection()
        cur = sql.cursor()
        res_headshot = cur.execute(
            "SELECT headshot FROM users WHERE username = ?", (username,)
        ).fetchone()
        sql.commit()
        sql.close()
        if res_headshot:
            return res_headshot[0]

        return None


class BlogHeader:
    def __init__(
        self, *, blog_id: int, title: str, tags: str, created_at: str, updated_at: str
    ) -> None:
        self.id = blog_id
        self.title = title
        self.tags = tags
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class BlogDto:
    def __init__(
        self, *, blog_id: int, title: str, tags: str, content: str, created_at: str, updated_at: str
    ) -> None:
        self.id = blog_id
        self.title = title
        self.tags = tags
        self.created_at = created_at
        self.updated_at = updated_at
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "tags": self.tags,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Blog:
    @classmethod
    def list_all(cls, username: str) -> List[BlogHeader]:
        sql = connection()
        cur = sql.cursor()
        res_blogs = cur.execute(
            """SELECT id, title, tags, created_at, updated_at
            FROM blogs
            WHERE state = ? AND username = ?
            """,
            (
                BlogState.ACTIVE.value,
                username,
            ),
        ).fetchall()
        sql.commit()
        sql.close()
        if res_blogs:
            blog_headers = [
                BlogHeader(
                    blog_id=b[0],
                    title=b[1],
                    tags=b[2].split(","),
                    created_at=b[3],
                    updated_at=b[4],
                )
                for b in res_blogs
                if b
            ]
            return blog_headers

        return []

    @classmethod
    def get(cls, username: str, blog_id: int) -> Optional[BlogDto]:
        print("hello...", blog_id)
        sql = connection()
        cur = sql.cursor()
        res_blog = cur.execute(
            """SELECT id, title, tags, content, created_at, updated_at
            FROM blogs
            WHERE id = ? AND state = ? AND username = ?
            """,
            (
                blog_id,
                BlogState.ACTIVE.value,
                username,
            ),
        ).fetchone()
        sql.commit()
        sql.close()
        print(res_blog)
        if res_blog:
            print("here...", res_blog)
            return BlogDto(
                blog_id=res_blog[0],
                title=res_blog[1],
                tags=res_blog[2].split(","),
                content=json.loads(res_blog[3]),
                created_at=res_blog[4],
                updated_at=res_blog[5],
            )

        return None

    @classmethod
    def add(cls, username: str, title: str, tags: List[str], content: Dict[str, Any]) -> None:
        if not tags:
            tags = ""

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        sql = connection()
        cur = sql.cursor()
        cur.execute(
            """
            INSERT INTO blogs(username, title, tags, content, state, created_at, updated_at)
            VALUES(?, ?, ?, ?, ?, ?, ?);
            """,
            (
                username,
                title,
                ",".join(tags),
                json.dumps(content),
                BlogState.ACTIVE.value,
                now,
                now,
            ),
        )
        sql.commit()
        sql.close()

    @classmethod
    def delete(cls, username: str, blog_id: int) -> None:
        sql = connection()
        cur = sql.cursor()
        cur.execute(
            "UPDATE blogs SET state = ? WHERE username = ? AND id = ?;",
            (
                BlogState.DELETED.value,
                username,
                blog_id,
            ),
        )
        sql.commit()
        sql.close()


class AddBlogDto:
    def __init__(
        self,
        *,
        title: str,
        tags: List[str],
        content: Dict[str, Any],
    ) -> None:
        self.title = title

        if not tags:
            tags = ""

        self.tags = "".join(tags)
        self.content = json.dumps(content)


class MigrationVersion:
    @classmethod
    def get(cls) -> str:
        sql = connection()
        cur = sql.cursor()
        res = cur.execute("SELECT version FROM migration_versions;")
        version = res.fetchone()
        if version:
            return version[0]

        return None
