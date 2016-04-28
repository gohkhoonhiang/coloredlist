### Table of Contents

* [Introduction](#introduction)
* [Getting Started](#getting-started)
..* [Virtual Environment](#virtual-environment)
..* [Installing Packages](#installing-packages)
* [Creating the App](#creating-the-app)
..* [The Main Application](#the-main-application)
..* [Templates](#templates)
* [Creating the List](#creating-the-list)
..* [List URL Mapping](#list-url-mapping)
..* [In Memory Storage](#in-memory-storage)
..* [Import UUID](#import-uuid)
..* [List Template](#list-template)
..* [List Handler](#list-handler)
* [Edit and Delete List Items](#edit-and-delete-list-items)
..* [List Item URL Mapping](#list-item-url-mapping)
..* [List Item Handler](#list-item-handler)
..* [Importing Javascript](#importing-javascript)
..* [Edit Template](#edit-template)
..* [AJAX](#ajax)


# Introduction

This is a prototype as part of learning Tornado framework. The idea and design of the app is based off [here](https://css-tricks.com/app-from-scratch-1-design/).

I will attempt to write the README in tutorial style, as how I taught myself doing it from various sources.

I will also try to commit the README and source code in accordance to the progress of the application.

Hopefully this will make it easier to follow the README and source code at different stages.

*Please feel free to file issues regarding the README if you find something inaccurate or unclear about the explanation. This is my first time writing a public tutorial and I have a lot to learn from anyone of you who care enough to read this. Thank you so much for your support.*

*Also, please do file issues regarding the actual source code if you find the code does not comply with certain standards or if improvements are needed. I am still new to python and there will surely be coding style which I have not followed.*

[Back to top](#table-of-contents)

# Getting Started

## Virtual Environment

As this is a python-based app, it is recommended to use `virtualenv` to contain the necessary packages for this project only.

Run `pip install virtualenv` to install `virtualenv` if you don't already have the package.

In the directory you have created for this project, run the command `virtualenv venv` to create the directory for the new environment. Replace `venv` with any name you wish.

*If you want to use python3 for the project, run `virtualenv -p python3 venv` instead. Make sure you already have python3 installed.*

To activate the environment, run the command `. venv/bin/activate` in the directory you have created `venv` directory.

You should see that your command prompt has `(venv)` in the prefix.

You can read more about `virtualenv` [here](https://virtualenv.readthedocs.org).

[Back to top](#table-of-contents)

## Installing Packages

The packages required for getting started with developing this app is included in the `requirements.txt` file.

Run `pip install -r requirements.txt` to install the packages.

You can read more about python package installation [here](https://pip.pypa.io/en/stable/user_guide/).

[Back to top](#table-of-contents)

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

[Back to top](#table-of-contents)

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

[Back to top](#table-of-contents)

# Creating the List

We now have a basic structure application. It's time to start creating the list itself.

We will start with just 2 simple functionalities for the list.
* View the list
* Create a list item

[Back to top](#table-of-contents)

## List URL Mapping

For each of the functionalities above, we will design endpoints for the client to send the requests to.

In the `make_app()` method we created earlier, we will add a few more `URLSpec` objects for each endpoint.

```
def make_app():
    return tornado.web.Application([
        url(r"/", MainHandler),
        url(r"/list/create", ListHandler),
        url(r"/list", ListHandler),
    ],
    debug=True)
```

[Back to top](#table-of-contents)

## In Memory Storage

For the time being, we will not use a persistent database for storage. Instead, we will create a in-memory storage for our list items.

We will come to using persistent storage at a later stage. For now, our purpose is to get the logic working.

We declare a global variable `list_items` that we will use as a in-memory storage for all the list items.

We will define it as a dictionary where the item ID will be the key and the item definition is another dictionary that forms the value paired with the key.

```
list_items = {
    "1":{"id":"1","text":"Walk the dog","color":"Red"},
    "2":{"id":"2","text":"Pick up dry cleaning","color":"Blue"},
    "3":{"id":"3","text":"Milk","color":"Green"},
}
```

We initialize some data first that we can display in the front-end.

[Back to top](#table-of-contents)

## Import UUID

For the purpose of using `uuid` to generate a unique ID for each item, we need to remember to import the `uuid` module.

```
import uuid
```

[Back to top](#table-of-contents)

## List Template

To help us visualize the data, let's create the `list.html` template file first.

```
<ul>
{% for item_id in items %}
    <li class="{{ items[item_id]["color"] }}">
        <span>{{ items[item_id]['text'] }}</span>
    </li>
{% end %}
</ul>

<form action="/list/create" method="post">
    <div>
        <input type="text" id="new-list-item-text" name="text">
        <input type="submit" id="new-item-submit" value="Add" class="button">
    </div>
</form>
```

Notice something different is happening in this template. We have injected some python code in this template to help us display the list items.

Since we are going to have a list of items, it is logical to have a loop control to display each item. This is where we use the `{% for item_id in items %}` construct.

In our in-memory store, we use the item ID as the key for the item definition itself, so in order to access the item data, we will need to get the item dictionary and then the attribute.

For example, we will use `{{ items[item_id]["text"] }}` to retrieve the text of the item with a specific `item_id`.

We have not added all the `<head>` and `<body>` tags in this template, because we are going to make use of template inheritance later.

For now we just want to make sure the data are displayed correctly with this structure.

This template should display a list of items in storage, and also provide a form to allow creating a new item which will be added to the in-memory storage.

[Back to top](#table-of-contents)

## List Handler

We will not use the `MainHandler` for handling requests pertaining to the list. Instead, we will create a new `ListHandler` class for this purpose.

For each of the functionalities, we assign a method in the `ListHandler` according to the HTTP method we allow for access.

```
class ListHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("list.html", items=list_items)

    def post(self):
        text = self.get_body_argument("text")
        item_id = str(uuid.uuid4())
        list_items[item_id] = {"id":item_id,"text":text,"color":"Blue"}
        self.redirect("/list")
```
As the client requests for `http://server:port/list`, the `ListHandler`'s `get` method will render the `list.html` page.

If the client enters some text in the form and hit the `Add` button, it will send a `POST` request containing the form data. The `ListHandler`'s `post` method will handle this request.

First we will extract the text entered by the client by calling `self.get_body_argument("text")`. Note that all form data are accessible by `self.get_body_argument` method by passing in the input name as the method parameter.

We will auto-generate a unique ID for this item by using `uuid.uuid4()` method.

Then we create a new dictionary containing all the item data and add it to the in-memory `list_items` storage using the `item_id` as key.

Once we are done with the storage, we will redirect to the `/list` page so that the changes can be reflected to the user.

We will realize that the list items are not sorted according to the order they are created. For that, we will need to devise some data strucutre and logic to handle the sorting later.

[Back to top](#table-of-contents)

# Edit and Delete List Items

A list without the edit or delete functions are almost useless. We will now add these functionalities to our list.

There can be a few ways to approach this problem.

1. Continue using `ListHandler` and add the corresponding `put` and `delete` methods for editing and deleting list items.
2. Create a separate `ListItemEditHandler` and `ListItemDeleteHandler` for editing and deleting list items.

The first approach will be more compact due to having only a single handler. The methods also clearly reflects the purpose of the request, mapping edit to `put` and delete to `delete` methods.

However, we cannot simply use a form for editing and deleting, because HTML `<form>` does not support `put` and `delete` methods. We will need to use AJAX for these actions.

The second approach is more lengthy due to having to create 2 more handlers just for each of the actions.

However, we can easily use a form to send a `post` request for each actions, and map to a `post` method within each handler.

Personally, I would prefer doing the first approach. I only need to main a single handler, while having the advantage of mapping the actions correctly to the methods: edit to `put` and delete to `delete`.

[Back to top](#table-of-contents)

## List Item URL Mapping

For using the first approach, we will map the request URL as follows:

```
url(r"/list/([0-9a-zA-Z\-]+)/edit", ListHandler),
```

[Back to top](#table-of-contents)

## List Item Handler

Since it is an edit action, we will map it to the `put` method of the `ListHandler`.

```
def put(self, item_id):
    text = self.get_body_argument("text")
    item = None
    try:
        item = list_items[item_id]
    except KeyError:
        self.set_status(404)
        self.finish("Not found")
        return
    if item:
        item["text"] = text
    self.set_status(200)
    self.finish("OK")
    return
```

The `item_id` is already provided as a path argument. We only need to extract the `text` data from the request body by calling `self.get_body_argument` method.

To do a little error handling, we will try to get the item data from the `list_items` dictionary, while catching `KeyError`.

If `KeyError` is raised, then we will return a status of `404` and message `Not found` to inform the client of the error.

If the item is found, then we just overwrite the `text` value.

At the end of it, we will return a status of `200` and message `OK` to inform the client that the edit is done.

[Back to top](#table-of-contents)

## Importing Javascript

We can write plain Javascript for the AJAX calls, but I decide that it is best to use existing libraries to make our life easier.

We will use jQuery to help with handling the AJAX calls, so we will include this following code in the `list.html` file.

```
<script src="https://code.jquery.com/jquery-2.2.3.min.js" integrity="sha256-a23g1Nt4dtEYOj7bR+vTu7+T8VP13humZFBJNIYoEJo=" crossorigin="anonymous"></script>
```

We will add this `<script>` tag at the end of the page so that it does not slow down the page loading.

[Back to top](#table-of-contents)

## Edit Template

Then, we will need to cater for editing by changing the `list.html` file. Previously we have a simple `<span>{{ items[item_id]['text'] }}</span>` to display the item text. Now we need to make it editable.

```
<span><input type="hidden" id="edit-item-{{ item_id }}-id" value="{{ item_id }}"><input type="text" id="edit-item-{{ item_id }}-text" name="text" value="{{ items[item_id]['text'] }}"><a href="#" id="edit-item-{{ item_id }}-submit" class="button edit-button">Edit</a></span>
```

We have added a hidden field to store the `item_id`, put the item text in a text input field and created a link to submit the edit action.

Note that we have created a unique ID for each input field as there may be multiple of such fields in the same list.

[Back to top](#table-of-contents)

## AJAX

Now we have the fields ready, we need to add in the logic to send the data to the server.

Below the `<script>` tag that imports the jQuery source, we will create our customized Javascript that will perform the AJAX call.
 
```
<script type="text/javascript">
<script type="text/javascript">
$(document).ready(function() {
    $('.edit-button').click(function() {
        var itemSpan = $(this).parent();
        var itemId = $(itemSpan).find("input[type='hidden']").val();
        var text = $(itemSpan).find("input[name='text']").val();
        var url = "/list/" + itemId + "/edit";
        console.log(url);
        $.ajax({
            type: "PUT",
            url: url,
            dataType: "json",
            data: {"id": itemId, "text": text},
            statusCode: {
                200: function(xhr) {
                    alert("Item updated successfully");
                },
                404: function(xhr) {
                    alert("Item ID not found");
                },
            },
        });
    });
});
</script>
```

There is quite a lot going on in this segment of code.

First, we attach the `click` event to all the elements with the class `edit-button`. In this case, it will be all the `<a>` tags for each list item.

Once the `click` event is triggered, we will try to extract the data we require.

We get the parent `<span>` containing the `<a>` being clicked. This allows us to extract the element containing the `item_id` and `text` of the item.

Once we have these data, we can now construct the URL and data for the AJAX call.

Since we have defined a `put` method in the `ListHandler` to handle the edit function, we will set the call type to `PUT`. The data will be sent as a `json` data type and the data itself is constructed using the values from the input fields.

Once the server returns a response, we will display an alert to inform the status.

[Back to top](#table-of-contents)


