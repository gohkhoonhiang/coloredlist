from tornado.web import url
from handlers.main import MainHandler
from handlers.list import ListHandler
from handlers.auth import LoginHandler, LogoutHandler
from handlers.account import AccountHandler
from db import db


url_patterns = [
    url(r"/", MainHandler),
    url(r"/list/([0-9a-zA-Z\-]+)/edit", ListHandler, dict(db=db)),
    url(r"/list/([0-9a-zA-Z\-]+)/delete", ListHandler, dict(db=db)),
    url(r"/list/create", ListHandler, dict(db=db)),
    url(r"/list", ListHandler, dict(db=db)),
    url(r"/login", LoginHandler, dict(db=db)),
    url(r"/login/submit", LoginHandler, dict(db=db)),
    url(r"/logout", LogoutHandler, dict(db=db)),
    url(r"/account/create", AccountHandler, dict(db=db)),
    url(r"/account/create/submit", AccountHandler, dict(db=db)),
]
