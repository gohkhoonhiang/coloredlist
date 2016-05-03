from tornado.web import url
from handlers.main import MainHandler
from handlers.list import ListHandler
from db import db


url_patterns = [
    url(r"/", MainHandler),
    url(r"/list/([0-9a-zA-Z\-]+)/edit", ListHandler, dict(db=db)),
    url(r"/list/([0-9a-zA-Z\-]+)/delete", ListHandler, dict(db=db)),
    url(r"/list/create", ListHandler, dict(db=db)),
    url(r"/list", ListHandler, dict(db=db)),
]
