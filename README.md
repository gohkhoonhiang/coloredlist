# Introduction

This is a prototype as part of learning Tornado framework. The idea and design of the app is based off [here](https://css-tricks.com/app-from-scratch-1-design/).

I will attempt to write the README in tutorial style, as how I taught myself doing it from various sources.

I will also try to commit the README and source code in accordance to the progress of the application.

Hopefully this will make it easier to follow the README and source code at different stages.

*Please feel free to file issues regarding the README if you find something inaccurate or unclear about the explanation. This is my first time writing a public tutorial and I have a lot to learn from anyone of you who care enough to read this. Thank you so much for your support.*

*Also, please do file issues regarding the actual source code if you find the code does not comply with certain standards or if improvements are needed. I am still new to python and there will surely be coding style which I have not followed.*

# Getting Started

## Virtual Environment

As this is a python-based app, it is recommended to use `virtualenv` to contain the necessary packages for this project only.

Run `pip install virtualenv` to install `virtualenv` if you don't already have the package.

In the directory you have created for this project, run the command `virtualenv venv` to create the directory for the new environment. Replace `venv` with any name you wish.

*If you want to use python3 for the project, run `virtualenv -p python3 venv` instead. Make sure you already have python3 installed.*

To activate the environment, run the command `. venv/bin/activate` in the directory you have created `venv` directory.

You should see that your command prompt has `(venv)` in the prefix.

You can read more about `virtualenv` [here](https://virtualenv.readthedocs.org).

## Installing Packages

The packages required for getting started with developing this app is included in the `requirements.txt` file.

Run `pip install -r requirements.txt` to install the packages.

You can read more about python package installation [here](https://pip.pypa.io/en/stable/user_guide/).


# Creating the App

## The Main Application

We will start with a `app.py` file, which contains the basics of the application we want to create.

For now, we will not care about the application structure. Our goal here is just to get it to work.

We need to import some packages from the `tornado` framework.

```
import tornado.ioloop
import tornado.web
from tornado.web import url
```

We will use a function to create the application instead of writing it directly in the main code.

```
def make_app():
    return tornado.web.Application([
        url(r"/", MainHandler),
    ],
    debug=True)
```

We first define the main page URL and its handler. Whenever the client requests for `http://server:port/`, the `MainHandler` will handle the request and send the appropriate response.

The `debug=True` setting is to run the application in debug mode.

Now we will define the `MainHandler`.

```
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
```

When the client requests for `http://server:port/`, it will be sent as a `GET` request, so this will be handled by the `MainHandler`'s `get` function.

We will serve a HTML page as the response.

Notice that I have injected some CSS classes and defined some IDs in the HTML elements. We will come to styling later.

In order for the server to run, we need to define the main entry code.

```
if __name__ == '__main__':
    app = make_app()
    app.listen(9080)
    tornado.ioloop.IOLoop.current().start()
```

We need to create an instance of the application by calling the `make_app()` function. Then I make it listen to port 9080. You can choose whichever port you wish.

The server is started by `tornado.ioloop.IOLoop.current().start()`.


## Templates

It is a little messy to write the HTML code directly in the `MainHandler`'s `get` function. We will try to take this code out into a proper HTML file, and get the handler to render the HTML file.

We first create the `main.html` file and put the exact HTML code into this file.

```
<!DOCTYPE html>    
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
</html>
```

To render this HTML file, we use the `render` method of the `RequestHandler` class.

We replace the `get` method we wrote earlier with the following:

```
def get(self):
    self.render("main.html")
```

Now the code looks much cleaner as we separate the view out of the logic code.


