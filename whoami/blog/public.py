import starlette.requests
import starlette.routing
from starlette.responses import JSONResponse, Response

from whoami import db


async def list_all(request: starlette.requests.Request) -> Response:
    all_blogs = db.Blog.list_all(request.state.username)
    return JSONResponse([b.to_dict() for b in all_blogs], status_code=200)


async def get(request: starlette.requests.Request) -> Response:
    blog_id = request.path_params.get("id")
    if blog_id is not None:
        blog_found = db.Blog.get(request.state.username, blog_id)
        if blog_found:
            return JSONResponse(blog_found.to_dict(), status_code=200)

    return Response(content=b"not found", status_code=404, headers={}, media_type="text/plain")


routes = [
    starlette.routing.Route(
        path="/blog",
        endpoint=list_all,
        methods=["GET"],
    ),
    starlette.routing.Route(
        path="/blog/{id}",
        endpoint=get,
        methods=["GET"],
    ),
]
