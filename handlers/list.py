import tornado.web
from bson.objectid import ObjectId
import json


class ListHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        username = self.get_secure_cookie("user").decode("utf-8") if self.get_secure_cookie("user") else None
        if username:
            lists = self.db['lists']
            list_items = self.db['list_items']
            user_list = lists.find_one({'username': username})
            items = []
            if user_list:
                list_id = user_list['_id']
                self.set_secure_cookie("list_id", str(list_id))
                items_cursor = list_items.find({'list_id': list_id})
                if items_cursor is not None:
                    items = [item for item in items_cursor]
            self.render("list.html", items=items)
        else:
            self.render("login.html")

    def post(self):
        username = self.get_secure_cookie("user").decode("utf-8") if self.get_secure_cookie("user") else None
        response = {}
        if username:
            lists = self.db['lists']
            list_items = self.db['list_items']
            text = self.get_body_argument("text")
            if text:
                list_id = self.get_secure_cookie("list_id").decode("utf-8") if self.get_secure_cookie("list_id") else None
                if list_id:
                    list_items.insert_one({'list_id': ObjectId(list_id), 'text':text, 'color':"Blue", 'status':"Open"})
            response['status'] = 201
            response['redirectUrl'] = "/list"
            self.write(json.dumps(response))
        else:
            response['status'] = 403
            response['errorMsg'] = "Please login to access your list"
            response['redirectUrl'] = "/login"
            self.write(json.dumps(response))

    def put(self, item_id):
        username = self.get_secure_cookie("user").decode("utf-8") if self.get_secure_cookie("user") else None
        response = {}
        if username:
            lists = self.db['lists']
            list_items = self.db['list_items']
            text = self.get_body_argument("text")
            if text:
                list_id = self.get_secure_cookie("list_id").decode("utf-8") if self.get_secure_cookie("list_id") else None
                if list_id:
                    item = list_items.find({'_id': ObjectId(item_id)})
                    if item:
                        list_items.update_one({'_id':ObjectId(item_id)}, {'$set':{'text':text}})
                        response['status'] = 200
                        response['redirectUrl'] = "/list"
                        self.write(json.dumps(response))
                    else:
                        response['status'] = 404
                        response['errorMsg'] = "Item not found"
                        response['redirectUrl'] = "/list"
                        self.write(json.dumps(response))
                else:
                    response['status'] = 404
                    response['errorMsg'] = "List not in session. Please re-login"
                    response['redirectUrl'] = "/login"
                    self.write(json.dumps(response))
            else:
                response['status'] = 400
                response['errorMsg'] = "Empty list item text"
                response['redirectUrl'] = "/list"
                self.write(json.dumps(response))
        else:
            response['status'] = 403
            response['errorMsg'] = "Please login to access your list"
            response['redirectUrl'] = "/login"
            self.write(json.dumps(response))

    def delete(self, item_id):
        username = self.get_secure_cookie("user").decode("utf-8") if self.get_secure_cookie("user") else None
        response = {}
        if username:
            lists = self.db['lists']
            list_items = self.db['list_items']
            list_id = self.get_secure_cookie("list_id").decode("utf-8") if self.get_secure_cookie("list_id") else None
            if list_id:
                item = list_items.find({'_id': ObjectId(item_id)})
                if item:
                    list_items.remove({'_id':ObjectId(item_id)})
                    response['status'] = 200
                    response['redirectUrl'] = "/list"
                    self.write(json.dumps(response))
                else:
                    response['status'] = 404
                    response['errorMsg'] = "Item not found"
                    response['redirectUrl'] = "/list"
                    self.write(json.dumps(response))
            else:
                response['status'] = 404
                response['errorMsg'] = "List not in session. Please re-login"
                response['redirectUrl'] = "/login"
                self.write(json.dumps(response))
        else:
            response['status'] = 403
            response['errorMsg'] = "Please login to access your list"
            response['redirectUrl'] = "/login"
            self.write(json.dumps(response))


