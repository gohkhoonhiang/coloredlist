from handlers.base import BaseHandler


class MainHandler(BaseHandler):
    def initialize(self, db):
        super().initialize(db)

    def get(self):
        if not self.get_current_user():
            self.redirect("/login")
            return
        self.redirect("/list")


