import json

import starlette.requests
import starlette.routing
from starlette.responses import PlainTextResponse

from whoami import cache, db


async def user(request: starlette.requests.Request) -> PlainTextResponse:
    body = await request.body()
    json_body = json.loads(body)
    dto = db.UserDto(
        **json_body,
    )
    db.User.update(request.state.username, dto)
    return PlainTextResponse("ok")


async def user_headshot(request: starlette.requests.Request) -> PlainTextResponse:
    body = await request.body()
    json_body = json.loads(body)
    cache.Cache.expire_headshot()
    db.User.update_headshot(request.state.username, json_body["headshot"])
    cache.Cache.put_headshot(json_body["headshot"])
    return PlainTextResponse("ok")


routes = [
    starlette.routing.Route(
        path="/private/user",
        endpoint=user,
        methods=["POST"],
    ),
    starlette.routing.Route(
        path="/private/user/headshot",
        endpoint=user_headshot,
        methods=["POST"],
    ),
]
