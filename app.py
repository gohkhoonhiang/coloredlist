import tornado.ioloop
import tornado.web
from tornado.web import url


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")


def make_app():
    return tornado.web.Application([
        url(r"/", MainHandler),
    ],
    debug=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(9080)
    tornado.ioloop.IOLoop.current().start()


