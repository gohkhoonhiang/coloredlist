import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie("user"):
            self.redirect("/login")
            return
        self.redirect("/list")


