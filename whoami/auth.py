import typing

import base64

from passlib.context import CryptContext
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from whoami import config, db


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return PWD_CONTEXT.verify(plain_password, hashed_password)
    except Exception:
        return False


def authenticate(username: str, password: str) -> bool:
    hashed_password = db.User.get_hashed_password(username)
    return verify_password(password, hashed_password)


class Token:
    @classmethod
    def from_request(cls, request: Request) -> typing.Optional[str]:
        magic_number_auth = "Authorization"
        magic_number_basic = "Basic"
        auth = request.headers.get(
            magic_number_auth, request.headers.get(magic_number_auth.lower())
        )
        if auth is None:
            return None

        return auth[len(magic_number_basic) + 1 :]


class BasicAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        username = config.WHOAMI_USERNAME
        if request["path"].startswith("/private"):
            basic_auth = Token.from_request(request)
            decoded = base64.b64decode(basic_auth).decode("UTF-8")
            username, password = decoded.split(":")
            if not authenticate(username, password):
                return Response(
                    content=b"unauthorized",
                    status_code=401,
                    headers={},
                    media_type="text/plain",
                )

        request.state.username = username
        return await call_next(request)
