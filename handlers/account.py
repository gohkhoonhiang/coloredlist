import tornado.web
import hashlib
import json


class AccountHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        self.render("account_create.html")

    def post(self):
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        response = {}
        if username and password:
            users = self.db['users']
            lists = self.db['lists']
            if users.find_one({'username': username}):
                response['status'] = 400
                response['errorMsg'] = "User already exists"
                response['redirectUrl'] = "/account/create"
                self.write(json.dumps(response))
            else:
                hashed_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
                users.insert_one({'username': username, 'password': hashed_pass, 'is_admin': False, 'is_active': True})
                lists.insert_one({'list_name':"Default", 'username': username, 'share_link': ""})
                self.set_secure_cookie("user", username)
                response['status'] = 201
                response['redirectUrl'] = "/list"
                self.write(json.dumps(response))
        else:
            response['status'] = 400
            response['errorMsg'] = "Invalid username or password"
            response['redirectUrl'] = "/account/create"
            self.write(json.dumps(response))

            
