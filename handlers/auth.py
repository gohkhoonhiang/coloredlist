import tornado.web
import json


class LoginHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        self.render("login.html")

    def post(self):
        self.set_secure_cookie("user", self.get_argument("username"))
        self.redirect("/list")

class LogoutHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def post(self):
        response = {}
        if self.get_secure_cookie("user"):
            self.set_secure_cookie("user", "")
            response["status"] = 200
            response["redirectUrl"] = "/login"
            self.write(json.dumps(response))
        else:
            response["status"] = 400
            response["errorMsg"] = "User not in session"
            response["redirectUrl"] = "/login"
            self.write(json.dumps(response))


