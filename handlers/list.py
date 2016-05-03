import tornado.web
from bson.objectid import ObjectId


class ListHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        list_items = self.db['lists']
        items = [item for item in list_items.find()]
        self.render("list.html", items=items)

    def post(self):
        list_items = self.db['lists']
        text = self.get_body_argument("text")
        list_items.insert_one({'text':text, 'color':'Blue'})
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


