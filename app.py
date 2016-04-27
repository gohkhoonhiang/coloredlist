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

    def put(self, item_id):
        text = self.get_body_argument("text")
        item = None
        try:
            item = list_items[item_id]
        except KeyError:
            self.set_status(404)
            self.finish("Not found")
            return
        if item:
            item["text"] = text
        self.set_status(200)
        self.finish("OK")
        return


def make_app():
    return tornado.web.Application([
        url(r"/", MainHandler),
        url(r"/list/([0-9a-zA-Z\-]+)/edit", ListHandler),
        url(r"/list/create", ListHandler),
        url(r"/list", ListHandler),
    ],
    debug=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(9080)
    tornado.ioloop.IOLoop.current().start()


