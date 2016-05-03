import tornado.ioloop
import tornado.web
from tornado.web import url
from pymongo import MongoClient
import os
from handlers.main import MainHandler
from handlers.list import ListHandler


def create_db():
    client = MongoClient("localhost",27017)
    db = client['coloredlistdb']
    return db
    

def make_app(db):
    return tornado.web.Application([
        url(r"/", MainHandler),
        url(r"/list/([0-9a-zA-Z\-]+)/edit", ListHandler, dict(db=db)),
        url(r"/list/([0-9a-zA-Z\-]+)/delete", ListHandler, dict(db=db)),
        url(r"/list/create", ListHandler, dict(db=db)),
        url(r"/list", ListHandler, dict(db=db)),
    ],
    debug=True,
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"))


if __name__ == '__main__':
    db = create_db()
    app = make_app(db)
    app.listen(9080)
    tornado.ioloop.IOLoop.current().start()


