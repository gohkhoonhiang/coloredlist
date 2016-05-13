import tornado.web
import hashlib
import json
from handlers.base import BaseHandler


class AccountHandler(BaseHandler):
    def initialize(self, db):
        super().initialize(db)

    def get(self):
        self.render("account_create.html")

    def post(self):
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        if username and password:
            users = self.db['users']
            lists = self.db['lists']
            if users.find_one({'username': username}):
                self.write_response_bad(errorMsg="User already exists", redirectUrl="/account/create")
            else:
                hashed_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
                users.insert_one({'username': username, 'password': hashed_pass, 'is_admin': False, 'is_active': True})
                lists.insert_one({'list_name':"Default", 'username': username, 'share_link': ""})
                self.set_current_user(username)
                self.write_response_created(redirectUrl="/list")
        else:
            self.write_response_bad(errorMsg="Invalid username or password", redirectUrl="/account/create")

            
