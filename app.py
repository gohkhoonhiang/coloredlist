import tornado.ioloop
import tornado.web
from tornado.web import url


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''<!DOCTYPE html>    
                    <html>
                    <head>
                        <title>Colored List App</title>
                    </head>
                    <body>
                        <div id="page-wrap">
                            <div id="header">
                                <h1><a href="/">Colored List App</a></h1>
                                <div id="control">
                                    <p><a href="/logout" class="button">Log Out</a>&nbsp;<a href="/account" class="button">Your Account</a></p>
                                    <p><a href="/signup" class="button">Sign Up</a>&nbsp;<a href="/login" class="button">Log In</a></p>
                                </div>
                            </div>
                            <div id="ribbon">
                                Reminders
                                <ul>
                                    <li>Your list automatically saves</li>
                                    <li>Double-click list items to edit them</li>
                                </ul>
                            </div>
                            <div id="main">
                            </div>
                        </div>
                    </body>
                    </html>''')


def make_app():
    return tornado.web.Application([
        url(r"/", MainHandler),
    ],
    debug=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(9080)
    tornado.ioloop.IOLoop.current().start()


