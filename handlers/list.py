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
        list_items = self.db['lists']
        text = self.get_body_argument("text")
        list_items.insert_one({'text':text, 'color':"Blue"})
        self.redirect("/list")

    def put(self, item_id):
        list_items = self.db['lists']
        text = self.get_body_argument("text")
        item = list_items.find_one({'_id':ObjectId(item_id)})
        if item:
            list_items.update_one({'_id':ObjectId(item_id)}, {'$set':{'text':text}})
            self.set_status(200)
            self.finish("OK")
            return
        else:
            self.set_status(404)
            self.finish("Not found")
            return

    def delete(self, item_id):
        list_items = self.db['lists']
        item = list_items.find_one({'_id':ObjectId(item_id)})
        if item:
            list_items.remove({'_id':ObjectId(item_id)})
            self.set_status(200)
            self.finish("OK")
            return
        else:
            self.set_status(404)
            self.finish("Not found")
            return


