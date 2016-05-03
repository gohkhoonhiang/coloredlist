import tornado.ioloop
import tornado.web
from tornado.web import url
from pymongo import MongoClient
import os
from handlers.main import MainHandler
from handlers.list import ListHandler
from settings import settings
from tornado.options import options


def create_db():
    client = MongoClient(options.dbhost, options.dbport)
    db = client[options.dbname]
    return db
    

def make_app(db):
    return tornado.web.Application([
        url(r"/", MainHandler),
        url(r"/list/([0-9a-zA-Z\-]+)/edit", ListHandler, dict(db=db)),
        url(r"/list/([0-9a-zA-Z\-]+)/delete", ListHandler, dict(db=db)),
        url(r"/list/create", ListHandler, dict(db=db)),
        url(r"/list", ListHandler, dict(db=db)),
    ],
    **settings)


if __name__ == '__main__':
    db = create_db()
    app = make_app(db)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


