import tornado.web
import json


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get_current_session(self):
        return self.get_current_user(), self.get_current_list()

    def set_current_session(self, user, list_id):
        self.set_secure_cookie("user", user)
        self.set_secure_cookie("list_id", list_id)

    def clear_current_session(self):
        self.set_current_session("", "")

    def get_current_user(self):
        return self.get_secure_cookie("user").decode("utf-8")

    def set_current_user(self, user):
        self.set_secure_cookie("user", user)

    def get_current_list(self):
        return self.get_secure_cookie("list_id").decode("utf-8")

    def set_current_list(self, list_id):
        self.set_secure_cookie("list_id", str(list_id))

    def write_response(self, status_code, **kwargs):
        response = {}
        response['status'] = status_code
        response['redirectUrl'] = kwargs['redirectUrl'] if 'redirectUrl' in kwargs else None
        response['errorMsg'] = kwargs['errorMsg'] if 'errorMsg' in kwargs else None
        self.write(json.dumps(response))

    def write_response_ok(self, **kwargs):
        self.write_response(200, **kwargs)
        
    def write_response_created(self, **kwargs):
        self.write_response(201, **kwargs)

    def write_response_bad(self, **kwargs):
        self.write_response(400, **kwargs)
        
    def write_response_forbidden(self, **kwargs):
        kwargs['redirectUrl'] = "/login"
        self.write_response(403, **kwargs)

    def write_response_not_found(self, **kwargs):
        self.write_response(404, **kwargs)



