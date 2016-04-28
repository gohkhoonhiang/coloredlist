import tornado.ioloop
import tornado.web
from tornado.web import url
from pymongo import MongoClient
from bson.objectid import ObjectId


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")


class ListHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        list_items = self.db['lists']
        items = [item for item in list_items.find()]
        self.render("list.html", items=items)

    def post(self):
        list_items = self.db['lists']
        text = self.get_body_argument("text")
        list_items.insert_one({'text':text, 'color':'Blue'})
        self.redirect("/list")

    def put(self, item_id):
        list_items = self.db['lists']
        text = self.get_body_argument("text")
        item = list_items.find_one({'_id':ObjectId(item_id)})
        if item:
            list_items.update_one({'_id':ObjectId(item_id)}, {'$set':{'text':text}})
            self.set_status(200)
            self.finish("OK")
            return
        else:
            self.set_status(404)
            self.finish("Not found")
            return

    def delete(self, item_id):
        list_items = self.db['lists']
        item = list_items.find_one({'_id':ObjectId(item_id)})
        if item:
            list_items.remove({'_id':ObjectId(item_id)})
            self.set_status(200)
            self.finish("OK")
            return
        else:
            self.set_status(404)
            self.finish("Not found")
            return


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
    debug=True)


if __name__ == '__main__':
    db = create_db()
    app = make_app(db)
    app.listen(9080)
    tornado.ioloop.IOLoop.current().start()


