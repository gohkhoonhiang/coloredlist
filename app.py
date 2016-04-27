import tornado.ioloop
import tornado.web
from tornado.web import url
import uuid


list_items = {
    "1":{"id":"1","text":"Walk the dog","color":"Red"},
    "2":{"id":"2","text":"Pick up dry cleaning","color":"Blue"},
    "3":{"id":"3","text":"Milk","color":"Green"},
}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")


class ListHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("list.html", items=list_items)

    def post(self):
        text = self.get_body_argument("text")
        item_id = str(uuid.uuid4())
        list_items[item_id] = {"id":item_id,"text":text,"color":"Blue"}
        self.redirect("/list")


def make_app():
    return tornado.web.Application([
        url(r"/", MainHandler),
        url(r"/list/create", ListHandler),
        url(r"/list", ListHandler),
    ],
    debug=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(9080)
    tornado.ioloop.IOLoop.current().start()


