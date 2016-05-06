import tornado.web
import hashlib


class AccountHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        self.render("account_create.html")

    def post(self):
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        if username and password:
            users = self.db['users']
            if users.find_one({'username': username}):
                self.render("account_error.html", reason="User already exists")
            else:
                hashed_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
                users.insert_one({'username': username, 'password': hashed_pass, 'is_admin': False, 'is_active': True})
                self.render("account_success.html")
        else:
            self.render("account_error.html", reason="Invalid username or password")

            
