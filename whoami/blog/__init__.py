from whoami.blog import private
from whoami.blog import public


routes = public.routes + private.routes
