from typing import Any, Dict, List
import json

import starlette.requests
import starlette.routing
from starlette.responses import Response, PlainTextResponse

from whoami import db


class AddBlogDto:
    def __init__(
        self,
        *,
        title: str,
        tags: List[str],
        content: Dict[str, Any],
    ) -> None:
        self.title = title
        self.tags = tags
        self.content = content


async def add_blog(request: starlette.requests.Request) -> Response:
    body = await request.body()
    blog_to_add = AddBlogDto(**json.loads(body))
    db.Blog.add(
        request.state.username,
        title=blog_to_add.title,
        tags=blog_to_add.tags,
        content=blog_to_add.content,
    )
    return PlainTextResponse("ok")


async def delete_blog(request: starlette.requests.Request) -> Response:
    blog_id = request.path_params.get("id")
    if blog_id is not None:
        db.Blog.delete(request.state.username, blog_id)
        return PlainTextResponse("ok")

    return Response(content=b"not found", status_code=404, headers={}, media_type="text/plain")


routes = [
    starlette.routing.Route(
        path="/private/blog",
        endpoint=add_blog,
        methods=["POST"],
    ),
    starlette.routing.Route(
        path="/private/blog/{id}",
        endpoint=delete_blog,
        methods=["DELETE"],
    ),
]
