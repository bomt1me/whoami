import base64
import io

import starlette.requests
import starlette.routing
from starlette.responses import JSONResponse, Response, StreamingResponse

from whoami import (
    cache,
    db,
)


async def user(request: starlette.requests.Request) -> Response:
    req_user = db.User.get(request.state.username)
    if req_user:
        return JSONResponse(req_user.to_dict(), status_code=200)

    return Response(content=b"not found", status_code=404, headers={}, media_type="text/plain")


async def headshot(request: starlette.requests.Request) -> Response:
    user_headshot_str = cache.Cache.get_headshot()
    if not user_headshot_str:
        user_headshot_str = db.User.get_headshot(request.state.username)
        if user_headshot_str:
            cache.Cache.put_headshot(user_headshot_str)

    if user_headshot_str:
        user_headshot = base64.b64decode(user_headshot_str)
        return StreamingResponse(io.BytesIO(user_headshot), media_type="image/svg+xml")

    return Response(content=b"not found", status_code=404, headers={}, media_type="text/plain")


routes = [
    starlette.routing.Route(
        path="/user",
        endpoint=user,
        methods=["GET"],
    ),
    starlette.routing.Route(
        path="/user/headshot",
        endpoint=headshot,
        methods=["GET"],
    ),
]
