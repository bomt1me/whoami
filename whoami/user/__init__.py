from whoami.user import private
from whoami.user import public


routes = public.routes + private.routes
