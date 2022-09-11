import starlette.applications
import starlette.middleware
import starlette.routing

from whoami import auth

from whoami import blog
from whoami import user


app = starlette.applications.Starlette(
    debug=False,
    routes=user.routes + blog.routes,
    middleware=[starlette.middleware.Middleware(auth.BasicAuthMiddleware)],
    exception_handlers={},
    on_startup=[],
    on_shutdown=[],
)
