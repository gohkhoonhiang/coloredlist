import tornado.web
import json
import hashlib


class LoginHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        self.render("login.html")

    def post(self):
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        users = self.db['users']
        response = {}
        if username and password:
            user = users.find_one({'username': username})
            if user:
                stored_pass = user['password']
                hashed_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
                if hashed_pass == stored_pass:
                    self.set_secure_cookie("user", username)
                    response['status'] = 200
                    response['redirectUrl'] = "/list"
                    self.write(json.dumps(response))
                else:
                    response['status'] = 403
                    response['errorMsg'] = "Invalid username or password"
                    response['redirectUrl'] = "/login"
                    self.write(json.dumps(response))
            else:
                response['status'] = 403
                response['errorMsg'] = "Invalid username or password"
                response['redirectUrl'] = "/login"
                self.write(json.dumps(response))
        else:
            response['status'] = 403
            response['errorMsg'] = "Invalid username or password"
            response['redirectUrl'] = "/login"
            self.write(json.dumps(response))

class LogoutHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def post(self):
        response = {}
        if self.get_secure_cookie("user"):
            self.set_secure_cookie("user", "")
            response['status'] = 200
            response['redirectUrl'] = "/login"
            self.write(json.dumps(response))
        else:
            response['status'] = 400
            response['errorMsg'] = "User not in session"
            response['redirectUrl'] = "/login"
            self.write(json.dumps(response))


