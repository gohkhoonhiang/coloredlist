### Table of Contents

* [Introduction](#introduction)
* [Getting Started](#getting-started)
  * [Virtual Environment](#virtual-environment)
  * [Installing Packages](#installing-packages)
* [Creating the App](#creating-the-app)
  * [The Main Application](#the-main-application)
  * [Templates](#templates)
* [Creating the List](#creating-the-list)
  * [List URL Mapping](#list-url-mapping)
  * [In Memory Storage](#in-memory-storage)
  * [Import UUID](#import-uuid)
  * [List Template](#list-template)
  * [List Handler](#list-handler)
* [Edit and Delete List Items](#edit-and-delete-list-items)
  * [List Item URL Mapping](#list-item-url-mapping)
  * [List Item Handler](#list-item-handler)
  * [Importing Javascript](#importing-javascript)
  * [Edit Template](#edit-template)
  * [AJAX](#ajax)
* [Persistent Storage](#persistent-storage)
  * [pymongo](#pymongo)
  * [Setting Up Database](#setting-up-database)
  * [Make Database](#make-database)
  * [Using Database](#using-database)
  * [List Template with New Data Structure](#list-template-with-new-data-structure)
* [Structuring the App](#structuring-the-app)
  * [Static Content](#static-content)
  * [Template Inheritance](#template-inheritance)
  * [Handlers Module](#handlers-module)
  * [App Settings](#app-settings)
  * [DB Settings](#db-settings)
  * [URL Patterns](#url-patterns)
  * [Final Structure](#final-structure)
* [Styling the App](#styling-the-app)
  * [Basic CSS](#basic-css)
* [User Authentication](#user-authentication)
  * [Login Form](#login-form)
  * [Login and Logout Handlers](#login-and-logout-handlers)
  * [Authentication URL Patterns](#authentication-url-patterns)
  * [Authentication AJAX](#authentication-ajax)
  * [Secret Cookie](#secret-cookie)
* [User Accounts](#user-accounts)
  * [New User Collection](#new-user-collection)
  * [Create Account Form](#create-account-form)
  * [Create Account Script](#create-account-script)
  * [After Create Account](#after-create-account)
  * [Create Account Handler and URL Mapping](#create-account-handler-and-url-mapping)
  * [Authenticate User with Password](#authenticate-user-with-password)
* [Revisit List and User Authentication](#revisit-list-and-user-authentication)
  * [Redefine List Collection](#redefine-list-collection)
  * [Create Default List for New User](#create-default-list-for-new-user)
  * [Authenticate User and Load List](#authenticate-user-and-load-list)
  * [Revisit List Item Operations](#revisit-list-item-operations)
* [Refactoring the App](#refactoring-the-app)
  * [Base Handler](#base-handler)
  * [Write Response](#write-response)
  * [Error Handling](#error-handling)


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
    '1':{'id':"1",'text':"Walk the dog",'color':"Red"},
    '2':{'id':"2",'text':"Pick up dry cleaning",'color':"Blue"},
    '3':{'id':"3",'text':"Milk",'color':"Green"},
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
    <li class="{{ items[item_id]['color'] }}">
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

For example, we will use `{{ items[item_id]['text'] }}` to retrieve the text of the item with a specific `item_id`.

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
        list_items[item_id] = {'id':item_id,'text':text,'color':"Blue"}
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
        item['text'] = text
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

# Persistent Storage

So far we have been using a in-memory storage for our list items. For this application to be useful, we need to persist the list data so that users can re-visit the list another day and the data will still be available.

Now we will look at how to integrate persistent storage in the application.

[Back to top](#table-of-contents)

## pymongo

There are a few databases that we can use for our application. I have chosen [MongoDB](https://www.mongodb.org/) for the simple reason that I want to learn how to use a NoSQL database. Please visit the official docs to learn how to setup a MongoDB instance on your machine for testing purpose.

In order to use Tornado with MongoDB, we need to have a database driver called [pymongo](http://api.mongodb.org/python/current/index.html).

We will add `pymongo==3.2.2` to our `requirements.txt` file so that we can install the module using pip.

After adding this line, don't forget to run the command `pip install -r requirements.txt` so that the pymongo package is installed.

[Back to top](#table-of-contents)

## Setting Up Database

After installing MongoDB and pymongo, we need to setup the database for our application's use.

We create a new database called `coloredlistdb` and create a new collection `lists`.

First, we run the `mongo` command to enter the MongoDB shell.

```
> mongo
MongoDB shell version: 3.2.5
connecting to: test
Welcome to the MongoDB shell.
For interactive help, type "help".
For more comprehensive documentation, see
    http://docs.mongodb.org/
Questions? Try the support group
    http://groups.google.com/group/mongodb-user
```

At this point, there is no database created yet, so we run the following command to initialize a database for `coloredlistdb`.

```
> use coloredlistdb
switched to db coloredlistdb
```

We will create a new collection to store our list items by running the following command.

```
> db.createCollection("lists")
{ "ok" : 1 }
```

We also initialize some data in the collection so that our application will display some items on first run.

```
> db.lists.insert({
... text:'Walk the dog',
... color:'Red'
... })
WriteResult({ "nInserted" : 1 })
> db.lists.insert({
... text:'Pick up dry cleaning',
... color:'Blue'
... })
WriteResult({ "nInserted" : 1 })
> db.lists.insert({
... text:'Milk',
... color:'Green'
... })
WriteResult({ "nInserted" : 1 })
```

To verify all the items have been inserted, we run the following command:

```
> db.lists.find()
{ "_id" : ObjectId("57220c6dcbe425b0c391538e"), "text" : "Walk the dog", "color" : "Red" }
{ "_id" : ObjectId("57220ccfcbe425b0c391538f"), "text" : "Pick up dry cleaning", "color" : "Blue" }
{ "_id" : ObjectId("57220cdccbe425b0c3915390"), "text" : "Milk", "color" : "Green" }
```

Notice that we have changed the data structure for list item. A MongoDB collection is analogous to a RDBMS table, each collection contains multiple documents, which is in turn analagous to RDBMS table rows. In MongoDB, each document is represented similar to JSON object.

For the purpose of our list items, we will define our data structure as follows:

```
{
    "_id" : item_id,
    "text" : item_text,
    "color" : item_color
}
```

[Back to top](#table-of-contents)

## Make Database

We can now start using the database from the application itself.

First of all, we need to import the required modules to use the pymongo driver.

```
from pymongo import MongoClient
from bson.objectid import ObjectId
```

We are going to use the `ObjectId` class for setting the item ID, so we can remove the `import uuid` statement.

Then we create a method to initialize the database and return the database object.

```
def create_db():
    client = MongoClient("localhost",27017)
    db = client['coloredlistdb']
    return db
```

In this method, we create a `MongoClient` that connects to `localhost` port `27017`.

Then we get the database of the name `coloredlistdb` as we have created earlier.

We will pass the database object to various request handlers for data storage and retrieval.

Since we create our URLSpec in the `make_app` method, we will pass the database object to the method in the main code.

```
if __name__ == '__main__':
    db = create_db()
    app = make_app(db)
```

Inside the `make_app` method, we will pass the database object to each URLSpec as follows:

```
def make_app(db):
    return tornado.web.Application([
        url(r"/", MainHandler),
        url(r"/list/([0-9a-zA-Z\-]+)/edit", ListHandler, dict(db=db)),
        url(r"/list/([0-9a-zA-Z\-]+)/delete", ListHandler, dict(db=db)),
        url(r"/list/create", ListHandler, dict(db=db)),
        url(r"/list", ListHandler, dict(db=db)),
    ],
    debug=True)
```

Then inside the `ListHandler` class, we need to add a `initialize` method to accept the database object and assign to its own `db` variable.

```
def initialize(self, db):
    self.db = db
```

[Back to top](#table-of-contents)

## Using Database

Since now that we have the database object in the `ListHandler`, we no longer use the in-memory storage.

Instead, we will get the list by calling `self.db['lists']`.

We will need to update all `get`, `post`, `put` and `delete` methods to use this database object.

```
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
```

Let's break it down a little and explain some of the new code.

In the `get` method, we get the collection object by calling `self.db['lists']`. To retrieve the documents, we need to get a cursor to the dataset by calling `list_items.find`, which is like a iterator to the documents. We use list comprehension construct `[item for item in list_items.find()]` to collect the documents into a list that can be used to render the `list.html` page.

For the `post` method, we will call the list_items.insert_one` method, passing in the dictionary containing the item text and color as parameter. The `_id` field will be automatically generated.

For the `put` method, we will first call `list_items.find_one` and pass in the `ObjectId(item_id)` as the query filter. This will return us only one result or none. If the result is not none, then we will update the collection and setting a new `text value for the document with `_id` `ObjectId(item_id)`.

Finally in the `delete` method, similar to the `put` method, we first query the collection to get the document with the same `ObjectId(item_id)`, then we simply call `list_items.remove` to delete the document from the collection.

Notice that we cannot simply pass the plain `item_id` string as the `_id` value, instead, we need to create a new `ObjectId` object with the `item_id`.

[Back to top](#table-of-contents)

## List Template with New Data Structure

Since we have changed the data structure of the list item, we also need to update the list view to reflect the changes.

```
{% for item in items %}
    <li class="{{ item['color'] }}">
        <span><input type="hidden" id="edit-item-{{ item['_id'] }}-id" value="{{ item['_id'] }}"><input type="text" id="edit-item-{{ item['_id'] }}-text" name="text" value="{{ item['text'] }}"><a href="#" id="edit-item-{{ item['_id'] }}-submit" class="button edit-button">Edit</a><a href="#" id="delete-item-{{ item['_id'] }}-submit" class="button delete-button">Delete</a></span>
    </li>
{% end %}
```

Instead of iterating through the IDs as in the earlier version, we now can iterate through the list of items directly.

To access the `text` and `value` attributes, we just call `item['text']` or `item['color']`.

Previously, we have not included the `Delete` function. Now we will add the AJAX call for deleting the item. It is similar in structure to the edit AJAX call, except that here we are using type `DELETE` and there is no need to send any data in the request.

```
$('.delete-button').click(function() {
    var itemSpan = $(this).parent();
    var itemId = $(itemSpan).find("input[type='hidden']").val();
    var text = $(itemSpan).find("input[name='text']").val();
    var url = "/list/" + itemId + "/delete";
    console.log(url);
    $.ajax({
        type: "DELETE",
        url: url,
        dataType: "json",
        data: {},
        statusCode: {
            200: function(xhr) {
                alert("Item deleted successfully");
                window.location.href = "/list";
            },
            404: function(xhr) {
                alert("Item ID not found");
            },
        },
    });
});
```

[Back to top](#table-of-contents)

# Structuring the App

Now we have a functional app where we can list items, add new item, edit and remove existing item.

However, the current structure is not the most ideal one. We have embedded Javascript directly in the `list.html` file, which makes it more difficult to maintain, and we cannot make use of caching to make our page load faster.

Ideally, we want to separate HTML, Javascript and CSS scripts into separate files, so that the browsers can cache unchanged `.js` and `.css` files, making page loading faster.

In the following sections, we will go through how to separate our Javascripts from the HTML pages.

[Back to top](#table-of-contents)

## Static Content

It is a common practice to create a `static` directory, containing `js`, `css` and `img` sub-directories. Each of these directories will contain Javascript, CSS and image files.

Then inside our HTML page, we will include them by using tags like `<script src=""></script>` for Javascript and `<link href="">` for CSS.

For our app, we will create `static` in the same directory as `app.py`, and contain `js`, `css` and `img` sub-directories like this:

```
+-- coloredlist/
|   +-- app.py
|   +-- static/
|   |   +-- css/
|   |   +-- img/
|   |   +-- js/
```

Then, we will create a new file `list.js` under the `static/js` directory, and extract the Javascript from `list.html` into this new file.

### `list.js`

```
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
    $('.delete-button').click(function() {
        var itemSpan = $(this).parent();
        var itemId = $(itemSpan).find("input[type='hidden']").val();
        var text = $(itemSpan).find("input[name='text']").val();
        var url = "/list/" + itemId + "/delete";
        console.log(url);
        $.ajax({
            type: "DELETE",
            url: url,
            dataType: "json",
            data: {},
            statusCode: {
                200: function(xhr) {
                    alert("Item deleted successfully");
                    window.location.href = "/list";
                },
                404: function(xhr) {
                    alert("Item ID not found");
                },
            },
        });
    });
});
```

### `list.html`

```
<script src="https://code.jquery.com/jquery-2.2.3.min.js" integrity="sha256-a23g1Nt4dtEYOj7bR+vTu7+T8VP13humZFBJNIYoEJo=" crossorigin="anonymous"></script>
<script src="{{ static_url('js/list.js') }}"></script>
```

Notice that we are using `static_url()` for the `list.js` URL formation, which will return the `list.js` relative to the static file path defined in our application as follows:

```
def make_app(db):
    return tornado.web.Application([
        url(r"/", MainHandler),
        url(r"/list/([0-9a-zA-Z\-]+)/edit", ListHandler, dict(db=db)),
        url(r"/list/([0-9a-zA-Z\-]+)/delete", ListHandler, dict(db=db)),
        url(r"/list/create", ListHandler, dict(db=db)),
        url(r"/list", ListHandler, dict(db=db)),
    ],
    debug=True,
    static_path=os.path.join(os.path.dirname(__file__), "static"))
```

[Back to top](#table-of-contents)

## Template Inheritance

Previously we made a note about template inheritance when we were making the list page. Now we have finally come to this part where we are going to make some base templates that can be extended by various pages.

First of all, we need to create a new directory `templates` in the same directory as `app.py`. Then we need to inform our application to load templates from the `templates` directory through the `template_path` setting:

```
def make_app(db):
    return tornado.web.Application([
        url(r"/", MainHandler),
        url(r"/list/([0-9a-zA-Z\-]+)/edit", ListHandler, dict(db=db)),
        url(r"/list/([0-9a-zA-Z\-]+)/delete", ListHandler, dict(db=db)),
        url(r"/list/create", ListHandler, dict(db=db)),
        url(r"/list", ListHandler, dict(db=db)),
    ],
    debug=True,
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"))
```

We now create a new file called `base.html`. Basically what this file will contain is the entire HTML markup of `main.html` with some additions, and it will be the base of all our pages.

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
        {% block content %}
        {% end %}
        </div>
    </div>
</body>
</html>
```

Under `<div id="main">`, we add the Python expressions:

```
{% block content %}
{% end %}
```

This allow us to extend the `base.html` template and put various page contents within this `div`.

We also need to move our `main.html` and `list.html` into the newly created `templates` directory.

Now we can extend `base.html` in `list.html` like this:

```
{% extends "base.html" %}
{% block content %}
<ul>
{% for item in items %}
    <li class="{{ item['color'] }}">
        <span><input type="hidden" id="edit-item-{{ item['_id'] }}-id" value="{{ item['_id'] }}"><input type="text" id="edit-item-{{ item['_id'] }}-text" name="text" value="{{ item['text'] }}"><a href="#" id="edit-item-{{ item['_id'] }}-submit" class="button edit-button">Edit</a><a href="#" id="delete-item-{{ item['_id'] }}-submit" class="button delete-button">Delete</a></span>
    </li>
{% end %}
</ul>

<form action="/list/create" method="post">
    <div>
        <input type="text" id="new-list-item-text" name="text">
        <input type="submit" id="new-item-submit" value="Add" class="button">
    </div>
</form>

<script src="https://code.jquery.com/jquery-2.2.3.min.js" integrity="sha256-a23g1Nt4dtEYOj7bR+vTu7+T8VP13humZFBJNIYoEJo=" crossorigin="anonymous"></script>
<script src="{{ static_url('js/list.js') }}"></script>
{% end %}
```

First, we need to indicate that we are extending from `base.html` by the expression `{% extends "base.html" %}`.

Then we indicate that we will extend the `{% block content %}` block by including our original `list.html` markup under `{% block content %}{% end %}` block.

When we load our `/list` page, we will have all the markup from `base.html` including `<div class="header">` and `<div class="ribbon">`, followed by the `{% block content %}` block, which will include `<ul>` and `<form>`.

For `main.html`, since we have just basically migrated the entire markup into `base.html`, we can just extend `base.html` directly inside `main.html` like this:

```
{% extends "base.html" %}
```

The advantage of template inheritance is that we don't need to copy-paste the header and footer everytime we create a new page with the same look-and-feel.

[Back to top](#table-of-contents)

## Handlers Module

The next thing we want to tackle here is `app.py`. Notice that it has grown in size pretty quickly even though have just started with 2 handlers. We want to make it easily maintainable, so we should start separating different handlers into their rightful places.

First, we need to create a new directory `handlers` in the same directory as `app.py`. Then we create `__init__.py` in `handlers` to indicate that it should be a `import`-able module.

We will migrate `class MainHandler` and `class ListHandler` into separate files, `main.py` and `list.py` respectively inside `handlers` directory.

What we have will be like this:

### `main.py`

```
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")
```

### `list.py`

```
import tornado.web
from bson.objectid import ObjectId


class ListHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        # ommitted for simplicity

    def post(self):
        # ommitted for simplicity

    def put(self, item_id):
        # ommitted for simplicity

    def delete(self, item_id):
        # ommitted for simplicity
```

Since we have extracted these 2 classes out of `app.py`, we need to tell the main application where to get the 2 handlers. For that, we need to import the 2 handlers from the newly created `handlers` module like this:

```
from handlers.main import MainHandler
from handlers.list import ListHandler
```

We don't need to change anything about the URLSpec definitions in creating the `tornado.web.Application` object.

[Back to top](#table-of-contents)

## App Settings

Our app is starting to look more structured than when we first started building it. We want to take a step further and make it more easily configurable by extracting all settings into a separate file called `settings.py`, which we will craete under the same directory as `app.py`.

```
import os
from tornado.options import define, options


# Define file paths
ROOT = os.path.join(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(ROOT, "static")
TEMPLATE_ROOT = os.path.join(ROOT, "templates")


# Define global options
define("port", default=9080, help="server port", type=int)
define("debug", default=True, help="debug mode")
define("dbhost", default="localhost", help="db host")
define("dbport", default=27017, help="db port", type=int)
define("dbname", default="coloredlistdb", help="name of db")


# Define application settings
settings = {}
settings['debug'] = options.debug
settings['static_path'] = STATIC_ROOT
settings['template_path'] = TEMPLATE_ROOT
```

In the newly created `settings.py` file, we will define the `STATIC_ROOT` and `TEMPLATE_ROOT` variables to be used in the application settings for `static_path` and `template_path` respectively.

We also make use of `tornado.options.options`, which is a global options object, to store certain options like `port` and `dbhost` etc by calling the `define` function.

Since we have extracted all the settings and options into a separate file, we need to tell our application how to load these settings and options. In our `app.py` file, we will need to import the `settings` object and `tornado.options.options` object:

```
from settings import settings
from tornado.options import options
```

Then we can make use of the settings and options like this:

```
def create_db():
    client = MongoClient(options.dbhost, options.dbport)
    db = client[options.dbname]
    return db

def make_app(db):
    return tornado.web.Application([
        url(r"/", MainHandler),
        url(r"/list/([0-9a-zA-Z\-]+)/edit", ListHandler, dict(db=db)),
        url(r"/list/([0-9a-zA-Z\-]+)/delete", ListHandler, dict(db=db)),
        url(r"/list/create", ListHandler, dict(db=db)),
        url(r"/list", ListHandler, dict(db=db)),
    ],
    **settings)

if __name__ == '__main__':
    db = create_db()
    app = make_app(db)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
```

By separating the settings and options from our application, we can make changes to the settings and options without having to change the `app.py` directly. It gives us the flexibility to deploy the application on different servers and using different databases by just dealing with `settings.py` file.

[Back to top](#table-of-contents)

## DB Settings

Since I've mentioned about using different databases for our app, we might as well make our app database-independent, meaning we shouldn't be tied to using only MongoDB, but have the option to use MySQL or PostgreSQL or whichever database deemed appropriate. For this, we have to restructure how we define our `db` object. Instead of creating the `db` object inside `app.py`, we will create a separate `db.py` under the same directory as `app.py`, where we will create a `db` object for our application's use.

```
from pymongo import MongoClient
from tornado.options import options


def create_db():
    client = MongoClient(options.dbhost, options.dbport)
    db = client[options.dbname]
    return db
    
db = create_db()
```

Then, we will remove the `create_db` function from `app.py`, and instead do a import of the `db` object:

```
from db import db
```

We can also remove the call to `create_db` in our main code:

```
if __name__ == '__main__':
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
```

We are not yet ready to be database-independent, but we will come to creating a database wrapper in a while.

[Back to top](#table-of-contents)

## URL Patterns

Honestly, I still haven't figured out why it is best practice to put URLs into a separate file. I guess it is probably for maintainability reasons. Personally I would also prefer defining the URLs separately from the main application, so that the `app.py` file will look clean and lean.

We will create a new `urls.py` file under the same directory as `app.py`. It will just contain our URLSpecs as follows:

```
from tornado.web import url
from handlers.main import MainHandler
from handlers.list import ListHandler
from db import db


url_patterns = [
    url(r"/", MainHandler),
    url(r"/list/([0-9a-zA-Z\-]+)/edit", ListHandler, dict(db=db)),
    url(r"/list/([0-9a-zA-Z\-]+)/delete", ListHandler, dict(db=db)),
    url(r"/list/create", ListHandler, dict(db=db)),
    url(r"/list", ListHandler, dict(db=db)),
]
```

Since we have extracted the URLs from `app.py`, we no longer need to import `db` and `handlers` in `app.py`, and the file should look like this now:

```
import tornado.ioloop
import tornado.web
from settings import settings
from tornado.options import options
from urls import url_patterns


def make_app():
    return tornado.web.Application(url_patterns, **settings)


if __name__ == '__main__':
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
```

[Back to top](#table-of-contents)

## Final Structure

At the end of all the restructuring, we should have achieved our desired structure for the application:

```
+-- coloredlist/
|   +-- app.py
|   +-- db.py
|   +-- settings.py
|   +-- urls.py
|   +-- handlers/
|   |   +-- __init__.py
|   |   +-- list.py
|   |   +-- main.py
|   +-- static/
|   |   +-- css/
|   |   +-- img/
|   |   +-- js/
|   |   |   +-- list.js
|   +-- templates/
|   |   +-- base.html
|   |   +-- list.html
|   |   +-- main.html
```

This may not be the best structure for a Tornado app, but we will improve on it as we add in more advanced features.

[Back to top](#table-of-contents)

# Styling the App

Since this is mainly a Tornado tutorial, I'm not going to focus much on styling the app. My purpose here is just to learn how to incorporate CSS files into my templates, so I'm going to take almost every CSS defined from the [sample](https://css-tricks.com/app-from-scratch-4-html-css/) and tweak such that there is no loading errors.

The end product is not going to look very nice, but that's really not our main concern here.

[Back to top](#table-of-contents)

## Basic CSS

Remember we have created our `static/css` folder earlier? Now we can put it into some use. Inside the directory, we will create 3 files, `main.css`, `list.css` and `sidebar.css`.

### `main.css`

Due to the file being quite loaded, I'm going to just extract a few lines here. For the complete CSS file, please refer to the source code.

```
* { margin: 0; padding: 0; }
body { font: 14px/1.1 Helvetica, Sans-Serif; }
.clear { clear: both; }
img, a img { border: none; }
input { outline: none; }
```

### `list.css`

```
#list { list-style: none; }
#list li { position: relative; margin: 0 0 8px 0; padding: 0 0 0 70px; width: 607px; }
#list li span { padding: 2px; -moz-border-radius: 5px; -webkit-border-radius: 5px; width: 589px; display: block; position: relative; }
```

### `sidebar.css`

```
#ribbon { position: absolute; right: 0; width: 125px; padding: 60px 30px 0 47px; height: 756px; top: -6px; }

#ribbon ul { list-style: none; }
#ribbon ul li { background: rgba(0,0,0,0.8); color: white; padding: 5px; margin: 0 0 5px 0; font-size: 12px; }
```

Then, we need to import the CSS files within the HTML templates like this:

### `base.html`

```
<head>
    <title>Colored List App</title>
    <link rel="stylesheet" href="{{ static_url('css/main.css') }}">
    <link rel="stylesheet" href="{{ static_url('css/sidebar.css') }}">
</head>
```

### `list.html`

```
{% block content %}
<link rel="stylesheet" href="{{ static_url('css/list.css') }}">
<ul id="list">
...
</ul>
<form id="add-new" action="/list/create" method="post">
    <div>
        <input type="text" id="new-list-item-text" name="text">
        <input type="submit" id="new-item-submit" value="Add" class="button">
    </div>
</form>
{% end %}
```

Note that for `list.html`, we have added an `id` attribute for the list `ul` element and `form` element. This is so that we can style them using our newly created stylesheets.

Now our app should have basic styling, although it most likely isn't very pleasant.

[Back to top](#table-of-contents)

# User Authentication

Notice that all this while we have been freely accessing our list without having to login at all. In this age where security is a concern, no one would use our app if it does not have any form of authentication. Now, we will start building in user authentication feature for our app.

[Back to top](#table-of-contents)

## Login Form

First of all, we will define our login form. It will be a simple form, with username and password fields.

```
{% extends "base.html" %}
{% block content %}
<form action="/login/submit" method="post">
    <div>
        <input type="text" name="username" id="username">
        <label for="username">Username</label>
        <input type="password" name="password" id="password">
        <label for="password">Password</label>
    </div>
    <input type="submit" id="login-submit" value="Login" class="button">
</form>
{% end %}
```

We will extend our `base.html` template and define the login form within `{% block content %}`.

There is nothing special about this form. We specify the action `/login/submit`, and will send the request as a `POST` request.

[Back to top](#table-of-contents)

## Login and Logout Handlers

We need to create handlers for our login form. We will create a new file `auth.py` under `handlers` directory, and create `class LoginHandler` inside the handler.

We will have a `get` function to handle `GET` request and `post` function to handle `POST` request. The `get` function will simply return our `login.html` form. When the login form sends a `POST` request, the `post` function will take the `username` from the request argument by calling `self.get_argument("username")`. We will set this username in our session cookie with `user` key, then redirect to the `/list` URL to display the list view.

For the time being, we will omit password authentication as this will require searching through the persistent datastore.

```
import tornado.web
import json


class LoginHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        self.render("login.html")

    def post(self):
        self.set_secure_cookie("user", self.get_argument("username"))
        self.redirect("/list")
```

For every authentication feature, there will be a logout function as well. We will then define another `class LogoutHandler` under `auth.py`.

```
class LogoutHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def post(self):
        response = {}
        if self.get_secure_cookie("user"):
            self.set_secure_cookie("user", "")
            response['status'] = 200
            response['redirectUrl'] = "/login"
            self.write(json.dumps(response))
        else:
            response['status'] = 400
            response['errorMsg'] = "User not in session"
            response['redirectUrl'] = "/login"
            self.write(json.dumps(response))
```

Basically, we will remove the user from our session cookie by setting the `user` key value to empty. Then we will create a response dictionary with `status=200` and `redirectUrl=/login`. However, if with any reason the user is no longer in session, we will return `status=400` with `errorMsg=User not in session` and `redirectUrl=/login`.

Since we now have an authentication feature, we must not forget to make sure our list page is *protected* against unauthenticated access. To do that, we have to modify our `MainHandler`'s `get` function as such:

```
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie("user"):
            self.redirect("/login")
            return
        self.redirect("/list")
```

What this does is that it will first check whether there is any user in the session cookie, and redirect to `/login` if there is no user, or to `/list` if user is still in session. Of course this is not very secure, we should check whether the request comes from the same user in session, but we will leave that to a later stage.

This is all very messy code and we shall come back later to refactor it. By then, we will need to introduce the concept of a `BaseHandler`. Let's come to that at a later stage.

[Back to top](#table-of-contents)

## Authentication URL Patterns

Once we have created our `LoginHandler` and `LogoutHandler`, we can map the handlers to the respect URLs.

Inside our `urls.py` file, we will add a new `import` statement:

```
from handlers.auth import LoginHandler, LogoutHandler
```

Then, we will add the mapping as such:

```
url(r"/login", LoginHandler, dict(db=db)),
url(r"/login/submit", LoginHandler, dict(db=db)),
url(r"/logout", LogoutHandler, dict(db=db)),
```

This is very straightforward by now. We will let `LoginHandler` handle `/login` and `/login/submit` URLs and `LogoutHandler` handle `/logout` URL.

[Back to top](#table-of-contents)

## Authentication AJAX

Remember we created a `Logout` button very early in our app development? We shall now put it into use.

In our `base.html`, we need to make a little change to our `Logout` button. Instead of calling `/logout` directly in the `a href` attribute, we need to use AJAX for the call, because `a href` only sends `GET` request.

```
<p><a href="#" id="logout-btn" class="button">Log Out</a>&nbsp;<a href="/account" class="button">Your Account</a></p>
```

To perform AJAX call, we will include the jQuery library and our `main.js` scripts at the bottom of `base.html`, before the closing `body` tag.

```
<script src="https://code.jquery.com/jquery-2.2.3.min.js" integrity="sha256-a23g1Nt4dtEYOj7bR+vTu7+T8VP13humZFBJNIYoEJo=" crossorigin="anonymous"></script>
<script src="{{ static_url('js/main.js') }}"></script>
```

Then inside `static/js` directory, we will create a new file for `main.js` and write our AJAX call.

```
$(document).ready(function() {
    $('#logout-btn').click(function() {
        $.ajax({
            type: "POST",
            url: "/logout",
            success: function(response) {
                if (response) {
                    response = JSON.parse(response);
                    if (response.status == 200) {
                        alert(response.errorMsg || "Logged out successfully.");
                    } else {
                        alert(response.errorMsg || "Error logging out");
                    }
                    window.location.href = response.redirectUrl;
                }
            }
        });
    }); 
});
```

We will attach a AJAX call to the `click` event of our `logout-btn`. This should send a `POST` request to the `/logout` URL.

On success, we will check for the response, we will parse into a JSON object for processing.

If the `response.status` is `200`, we will prompt the `response.errorMsg` or `Logged out successfully`. Otherwise, we will prompt the `response.errorMsg` or `Error logging out`.

In both cases, we will redirect the browser to the `response.redirectUrl` given by the server.

[Back to top](#table-of-contents)

## Secret Cookie

At the end of all this, there is one very important thing that we need to do for this authentication feature to work. We have to define a secret cookie key in our application, which is used to sign our cookies to prevent forgery.

This part is a bit tricky. The secret cookie key is supposed to be set in our `settings.py` file, but our application is open source, and everyone can see the `settings.py` source code. This means everyone will see our secret cookie key, and can as easily forge a cookie.

To solve this problem, we will have to define one configuration file to store the secret cookie key, and this file should never be made public and will only live in our server. Let's call the file `config.conf`. This file will store our secret cookie key in the form of `cookie_secret = 'some long string of characters'`.

Then our `settings.py` file will be modified to include reading the `config.conf` file and setting the `cookie_secret`:

```
import tornado
from tornado.options import define, options, parse_config_file 
```

First we will make additional imports for `parse_config_file`.

```
define("cookie_secret", default=None, help="secret cookie")
define("config", default="config.conf", help="secret config")
```

Then we will define the `cookie_secret` and `config` options. We will not be setting the `cookie_secret` directly here, instead we will make use of `config.conf` to read the value.

```
if options.config:
    if os.path.exists(options.config):
        parse_config_file(options.config)
```

To read the `config.conf` file, we will call the `parse_config_file` function, passing in the file name, which is defined in `options.config`.

```
settings['cookie_secret'] = options.cookie_secret
```

Finally, once we have read the option from `config.conf`, we can set it to our `settings['cookie_secret']`, which will be passed to the `Application` object during creation.

Now, our application is ready for authentication.

[Back to top](#table-of-contents)

# User Accounts

Based on our user authentication feature earlier, it doesn't really authenticate anyone, as it just stores the username in session without checking against the database whether the password is matching. We shall now create the concept of user accounts, so that we will have a database of users to authenticate against for every login.

[Back to top](#table-of-contents)

## New User Collection

To store user accounts in our database, we need to create a new collection called `users`. Let's start up our MongoDB client to create the collection.

```
> mongo
MongoDB shell version: 3.2.6
connecting to: test
> use coloredlistdb
switched to db coloredlistdb
>
```

We will call up the MongoDB shell using the `mongo` command. Then we switch to our database by `use coloredlistdb`.

```
> db.createCollection("users")
{ "ok" : 1 }
>
```

We will create a new collection to store our user accounts by running `db.createCollection("users")`.

Now we want create our first user account, let's make it the `admin` user. We are going to hash the password for this user, so we will need the help of the Python console. Let's call up `python`.

```
> python
Python 3.5.1+ (default, Mar 30 2016, 22:46:26)
[GCC 5.3.1 20160330] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import hashlib, pymongo
>>> hashed_pass = hashlib.md5("admin".encode("utf-8")).hexdigest()
>>> hashed_pass
'21232f297a57a5a743894a0e4a801fc3'
>>> client = pymongo.MongoClient("localhost", 27017)
>>> db = client.coloredlistdb
>>> users = db.users
>>> users.insert_one({'username': "admin", 'password': hashed_pass, 'is_active': True, 'is_admin': True})
<pymongo.results.InsertOneResult object at 0x7fe0779c7dc8>
>>>
```

In the Python console, we `import hashlib` which deals with hashing. Then we pass in our password `password` into the `hashlib.md5` function, but before that, we need to encode our `password` string with `encode("utf-8")`. Once the hash object is created, we call `hexdigest` to get the digest in hexadecimals digits. This is the string that we will use to store in the `users` collection.

Since we are using the Python console to generate the hashed password, we might as well use it to insert the user into our database. We create a `MongoClient` and get the `users` collection from the `coloredlistdb`. Then we insert the `admin` user with the following details:

```
{'username': "admin", 'password': hashed_pass, 'is_active': True, 'is_admin': True}
```

After this, if we query the database from the MongoDB shell, we should find the document created.

```
> db.users.find()
{ "_id" : ObjectId("572cbfceaeca133de672b178"), "is_admin" : true, "is_active" : true, "password" : "21232f297a57a5a743894a0e4a801fc3", "username" : "admin" }
>
```

[Back to top](#table-of-contents)

## Create Account Form

We will now create a new account form so that potential users can sign up for an account and start using our app. We will create `account_create.html` under `templates` directory.

```
{% extends "base.html" %}
{% block content %}
<h2>create account</h2>
<form action="/account/create/submit" method="post" id="account-create-form">
    <div>
        <input type="text" name="username" id="username">
        <label for="username">username</label>
        <input type="password" name="password" id="password">
        <label for="password">password</label>
        <input type="password" name="confirm-password" id="confirm-password">
        <label for="confirm-password">confirm password</label>
        <input type="submit" name="new-account-submit" id="new-account-submit" value="submit" class="button">
    </div>
</form>
<script src="https://code.jquery.com/jquery-2.2.3.min.js" integrity="sha256-a23g1Nt4dtEYOj7bR+vTu7+T8VP13humZFBJNIYoEJo=" crossorigin="anonymous"></script>
<script src="{{ static_url('js/account.js') }}"></script>
{% end %}
```

As usual, we will `{% extends "base.html" %}` and write our new account form within `{% block content %}`. We will create 3 fields for our purpose: `username`, `password` and `confirm-password`. The purpose of the `confirm-password` field is just to make sure the user has typed in the correct password, which we will validate using Javascript from `js/account.js` that we include at the end. Our form will `post` to `/account/create/submit` if the validation is successful.

We also change our `base.html` template to use the `/acccount/create` URL for `Sign Up`:

```
<p><a href="/account/create" class="button">Sign Up</a>&nbsp;<a href="/login" class="button">Log In</a></p>
```

[Back to top](#table-of-contents)

## Create Account Script

Now we create the Javascript that will handle the create account form submission. Create a new file `account.js` under `static/js` directory.

```
$(document).ready(function() {
    $('#new-account-submit').click(function(e) {
        if ($('#password').val() === $('#confirm-password').val()) {
            $('#account-create-form').submit();
        } else {
            e.preventDefault();
            alert('Password and Confirm Password do not match!');
        }
    });
});
```

For our Javascript, we will first take the `password` field value and match with `confirm-password` field value. If they match, we simply call `submit` function of the `account-create-form`.

However, if they don't match, we need to specifically call `e.preventDefault` so that the form submission will not happen. Then, we need to alert the user with a prompt, so that he can change the 2 password fields and make sure they match. 

[Back to top](#table-of-contents)

## After Create Account

We will also create the views that are displayed after successfully creating an account, or when the account is not created, perhaps due to duplicate username. Let's call them `account_success.html` and `account_error.html`.

### `account_success.html`

```
{% extends "base.html" %}
{% block content %}
<p>Your account has been created successfully. Please login at <a href="/login">Login Page</a> to start creating your list!</p>
{% end %}
```

There is nothing special in this page. We just `{% extends "base.html" %}` and then tell the user the account is created, and point to the Login Page.

### `account_error.html`

```
{% extends "base.html" %}
{% block content %}
<p>Error in creating your account. {% if reason %}{{ reason }}{% end %}</p>
<p>Please try again <a href="/account/create">here</a></p>
{% end %}
```

For the error page, there's an additional Python expression that checks for `reason` and display if it exists. Then we point to the New Account page again.

[Back to top](#table-of-contents)

## Create Account Handler and URL Mapping

We now create the handlers to handle the `get` and `post` requests of the account page, using a new file `account.py` under `handlers`.

```
import tornado.web
import hashlib


class AccountHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self):
        self.render("account_create.html")

    def post(self):
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        if username and password:
            users = self.db['users']
            if users.find_one({'username': username}):
                self.render("account_error.html", reason="User already exists")
            else:
                hashed_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
                users.insert_one({'username': username, 'password': hashed_pass, 'is_admin': False, 'is_active': True})
                self.render("account_success.html")
        else:
            self.render("account_error.html", reason="Invalid username or password")
```

Let's break this down. For the `get` function, it is just to render the `account_create.html` template. For the `post` function, we will first get the arguments `username` and `password` by calling `self.get_body_argument`. This will return us the values entered into the create account form.

We should always check that the `username` and `password` are not empty, then we will try to check whether the `username` already exists by calling `find_one` from our `users` collection. If it already exists, we will render the `account_error.html` template and pass in the `reason`. Otherwise,  we will hash the password using the `md5` algorithm from `hashlib` module. It is required by the hashing algorithm to encode our string, so we will call `encode("utf-8")` from the `password` string before passing it into the `md5` function. Finally, we get the hashed string by calling `hexdigest`, which will return us a string in hexadecimal digits. This hashed password together with the username will be inserted by calling `users.insert_one`. Note that we will set `is_admin` as `False` and `is_active` as `True` for the time being. Later when we add on an advanced feature to deal with locking user account, we can make use of the `is_active` attribute.

Finally, if we check that both `username` and `password` are empty, we will render the `account_error.html` template and pass in the `reason`.

The URLs mapping will be defined in `urls.py` as such:

```
from handlers.account import AccountHandler
```

First, we import the `AccountHandler` from `handlers.account`.

```
url(r"/account/create", AccountHandler, dict(db=db)),
url(r"/account/create/submit", AccountHandler, dict(db=db)),
```

Then we map `/account/create` and `/account/create/submit` to the `AccountHandler`.

[Back to top](#table-of-contents)

## Authenticate User with Password

Now that we have created `password` in our user accounts, we can change our authentication logic to validate login password against the database.

First, we need to make some changes to our `login.html` template.

```
{% extends "base.html" %}
{% block content %}
<form id="login-form">
    <div>
        <input type="text" name="username" id="username">
        <label for="username">Username</label>
        <input type="password" name="password" id="password">
        <label for="password">Password</label>
    </div>
    <input type="submit" id="login-submit" value="Login" class="button">
</form>
<script src="https://code.jquery.com/jquery-2.2.3.min.js" integrity="sha256-a23g1Nt4dtEYOj7bR+vTu7+T8VP13humZFBJNIYoEJo=" crossorigin="anonymous"></script>
<script src="{{ static_url('js/login.js') }}"></script>
{% end %}
```

*It's worth noting that we are now moving towards using AJAX for form submit, because we want to implement a RESTful server that returns JSON response. We will only use `<a>` tag for getting rendered response. Let's start refactoring our code from the authentication module, and we will refactor the rest of the application whenever necessary.* 

We have removed the `action` and `method` attributes of the `form`, instead, we will use AJAX to post the form data to the server, we are going to include the jQuery scripts and a new `js/login.js` file.

In the new `js/login.js` file, we will bind a function to the `login-submit` button's `click` event:

```
$(document).ready(function() {
    $('#login-submit').click(function(e) {
        e.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        if (username && password) {
            $.ajax({
                type: "POST",
                url: "/login/submit",
                dataType: "json",
                data: {"username":username, "password":password},
                success: function(response) {
                    if (response) {
                        if (response.status != 200 && response.errorMsg) {
                            alert(response.errorMsg || "Unable to login");
                        }
                        if (response.redirectUrl) {
                            window.location.href = response.redirectUrl;
                        }
                    }
                },
            });
        } else {
            alert("Please enter both username and password");
        }
    });
});
```

Since we are not going to do the traditional form submit, we will need to prevent the form submission by calling `e.preventDefault`. Then, we will extract the `username` and `password` fields, check that they are not empty and make the AJAX call to `/login/submit` with the `username` and `password` as form data. Upon successful request, we will get the `response` object and check the `status` code. If it is not `200`, we will try to display the `errorMsg`. If a `redirectUrl` is provided, we will redirect our page to the given URL.

We also try to validate that the `username` and `password` fields are entered, so we will prompt an error message for failing to enter either field, and we will not attempt to post the login details in this case.

Next, let's change our `handlers/auth.py` file to reflect the logic:

```
import tornado.web
import json
import hashlib


class LoginHandler(tornado.web.RequestHandler):
    # omitted code here
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        users = self.db['users']
        response = {}
        if username and password:
            user = users.find_one({'username': username})
            if user:
                stored_pass = user['password']
                hashed_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
                if hashed_pass == stored_pass:
                    self.set_secure_cookie("user", username)
                    response['status'] = 200
                    response['redirectUrl'] = "/list"
                    self.write(json.dumps(response))
                else:
                    response['status'] = 403
                    response['errorMsg'] = "Invalid username or password"
                    response['redirectUrl'] = "/login"
                    self.write(json.dumps(response))
            else:
                response['status'] = 403
                response['errorMsg'] = "Invalid username or password"
                response['redirectUrl'] = "/login"
                self.write(json.dumps(response))
        else:
            response['status'] = 403
            response['errorMsg'] = "Invalid username or password"
            response['redirectUrl'] = "/login"
            self.write(json.dumps(response))
```

We have a new `import hashlib` which will be in charge of hashing passwords.

There are quite a few changes in our `post` function. Now that we will validate the login username and password against the database, we will need to extract both fields from the request body by calling `self.get_body_argument`. We then get the `users` collection from `self.db`, and try to find the document with matching `username`. If the it is found, then we hash the `password` from the request body by using `hashlib.md5(password.encode("utf-8")).hexdigest` function. If this hashed password matches the password from the database, then we can set the user in our session cookie by `self.set_secure_cookie("user", username)`. For successful authentication, we return `response['status'] = 200` and `response['redirectUrl'] = "/list"`. To write the JSON response, we call `json.dumps(response)` and pass to `self.write`.

If the username or password is not provided, or if the username does not match any in our database, or if the password does not match, then we will return `response['status'] = 403`, `response['errorMsg'] = "Invalid username or password"` and `response['redirectUrl'] = "/login"`. `403` status code indicates `Forbidden`, and we provide a human-friendly error message `Invalid username or password`, then redirect the client back to `/login` URL.

Since we are refactoring our authentication module, let's also do some housekeeping on our logout AJAX call to make it consistent with our login AJAX call.

### `static/js/main.js`

```
$(document).ready(function() {
    $('#logout-btn').click(function() {
        $.ajax({
            type: "POST",
            url: "/logout",
            dataType: "json",
            data: {},
            success: function(response) {
                if (response) {
                    if (response.status != 200 && response.errorMsg) {
                        alert(response.errorMsg || "Error logging out");
                    }
                    if (response.redirectUrl) {
                        window.location.href = response.redirectUrl;
                    }
                }
            },
        });
    }); 
});
```

The logic is the same as before, only difference is that we specify the `dataType` to be `json` so that we don't have to `JSON.parse` the response. We also check that there is a `redirectUrl` and set the `window.location.href` accordingly.

[Back to top](#table-of-contents)

# Revisit List and User Authentication

Now that we have introduced the concept of an user account, we should revisit our list data structure and incorporate the concept of ownership for each list.

If we look at our previously defined `lists` collection, it is just a list of `item`s with `text` and `color`. However, this does not serve our purpose well. 

We will have to redefine our `lists` collection and assign a `username` to indicate ownership. Then we will create a separate collection just for `list_items`, and link back to the `lists` by the `lists`'s `_id`.

[Back to top](#table-of-contents)

## Redefine List Collection

First of all, let's remove the existing documents in the `lists` collection.

```
> mongo
MongoDB shell version: 3.2.6
connecting to: test
> use coloredlistdb
switched to db coloredlistdb
> db.lists.remove({})
WriteResult({ "nRemoved" : 5 })
> db.lists.find()
>
```

We will call up the MongoDB shell, switch to `coloredlistdb`, then run the `db.lists.remove` command. The `lists` collection should now be empty.

Then we will define a new data structure for our `lists` collection as such:

```
> db.lists.insert({
... list_name: "Default",
... username: "admin",
... share_link: "",
... })
WriteResult({ "nInserted" : 1 })
> db.lists.find()
{ "_id" : ObjectId("572d8d3909d5ea66b520225f"), "list_name" : "Default", "username" : "admin", "share_link" : "" }
>
```

We will let user name each list and store it in `list_name`. `username` will indicate that this list belongs to the username specified, for the time being, we will assign it to our `admin` user that we have created earlier. We will also have a `share_link` for publicly-accessible read-only view of the list.

Next, we will define a new collection `list_items` that will store the actual list item details.

```
> db.createCollection("list_items")
{ "ok" : 1 }
> db.list_items.insert({
... "list_id":ObjectId("572d8d3909d5ea66b520225f"),
... "text":"Walk the dog",
... "color":"Red",
... "status":"open",
... })
WriteResult({ "nInserted" : 1 })
>
```

Our `list_items` will have a link to the `lists` collection through the `list_id`. Then we put back the `text` and `color` fields from our previous definition. Finally, we add a new field `status` to indicate the status of the item, the default value is `open`.

We will insert 2 more default items with the same data structure and now our list should have the following items.

```
> db.list_items.find()
{ "_id" : ObjectId("572d903e3f9d3719da74684b"), "list_id" : ObjectId("572d8d3909d5ea66b520225f"), "text" : "Walk the dog", "color" : "Red", "status" : "open" }
{ "_id" : ObjectId("572d90f03f9d3719da74684c"), "list_id" : ObjectId("572d8d3909d5ea66b520225f"), "text" : "Pick up dry cleaning", "color" : "Blue", "status" : "open" }
{ "_id" : ObjectId("572d91053f9d3719da74684d"), "list_id" : ObjectId("572d8d3909d5ea66b520225f"), "text" : "Milk", "color" : "Green", "status" : "open" }
>
```

[Back to top](#table-of-contents)

## Create Default List for New User

Now that we have redefined our `lists` data strucutre, we need to link it up with our `users` in the create account logic.

```
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
```

Inside `handlers/account.py`, we will change the `post` function to add in the logic to create a default list for the new user. This is done by getting the `lists` collection from `self.db`, then perform a `lists.insert_one` with the `username` field being set to the new `username` from the sign up. We will also add the user directly in the session, and redirect to the `/list` page instead of showing them the `account_success.html` page.

Now, all new accounts will be assigned a default list and the users can immediately add new items to a list without having to login.

Similarly, if the account creation failed, we redirect them to the `/account/create` page with an error message, instead of showing them the `account_error.html` page, so that they can directly enter a new username without having to click a link to go back to the new account page.

With this change, we can remove `account_success.html` and `account_error.html` from `templates` directory.

As we change our back-end into a RESTful function, we also need to change our client `static/js/account.js`.

```
$(document).ready(function() {
    $('#new-account-submit').click(function(e) {
        e.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        var confirm_password = $('#confirm-password').val();
        if (username && password && confirm_password) {
            if (password === confirm_password) {
                $.ajax({
                    type: "POST",
                    url: "/account/create/submit",
                    dataType: "json",
                    data: {"username": username, "password": password},
                    success: function(response) {
                        if (response) {
                            if (response.status != 201 && response.errorMsg) {
                                alert(response.errorMsg || "Failed to create account");
                            }
                            if (response.redirectUrl) {
                                window.location.href = response.redirectUrl;
                            }
                        }
                    },
                });
            } else {
                alert("Password and Confirm Password do not match!");
            }
        } else {
            alert("Username, password and confirm password should not be empty");
        }
    });
});
```

Instead of the default form action, we will attach a function to the `new-account-submit`'s `click` event. We will call `e.preventDefault` to stop the submit action and use AJAX call to send a `POST` request to `/account/create/submit` with the `username` and `password` as data. Upon success, we will display any `errorMsg` and redirect to `redirectUrl` whenever available.

We should help users type the correct password by making sure the `password` and `confirm-password` fields match, or we will prmopt a message. To make sure we do not send empty `username` and `password`, we should prompt a message if the fields are empty.

[Back to top](#table-of-contents)

## Authenticate User and Load List

Now that we have linked up the user account with a list, we should load the correct list for each user who is authenticated successfully. When user has logged in and we redirect to the `/list` page, we need to get the corresponding list from the database.

For that, let's change our `handlers/list.py` file:

```
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
```

In the `get` function, we will get the `username` from session, then try to find the corresponding list by calling `lists.find_one({'username': username})`. If it is found, we will store the `list_id` in session, then retrieve the list of items from `list_items.find({'list_id': list_id})` and set to `items` variable in the `list.html` template.

In any case that the user has been logged out, we will simply render the `login.html` page so that the user can re-login to access the list.

On the other hand, if the user is no longer logged in, we should also remove the `list_id` from the secure_cookie store by changing the `LogoutHandler`:

```
def post(self):
    response = {}
    if self.get_secure_cookie("user"):
        self.set_secure_cookie("user", "")
        self.set_secure_cookie("list_id", "")
        response['status'] = 200
        response['redirectUrl'] = "/login"
        self.write(json.dumps(response))
    else:
        self.set_secure_cookie("list_id", "")
        response['status'] = 400
        response['errorMsg'] = "User not in session"
        response['redirectUrl'] = "/login"
        self.write(json.dumps(response))
```

[Back to top](#table-of-contents)

## Revisit List Item Operations

Since our list data structure has changed, we should also revisit our list operations.

### Add New Item

To store a new item to the `list_items` collection, we need to change our `handlers/list.py` file:

```
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
```

We need to make sure the user is in session by calling `self.get_secure_cookie("user")` and make sure it exists. Then we will retrieve the user's list by using the `list_id` in `self.get_seccure_cookie`, create a new list item using the given `text` in `self.get_body_argument("text")` and call `list_items.insert_one` to add the item to the list. If it's all successful, we will return `response['status'] = 201` and `response['redirectUrl'] = "/list"` to indicate `Created` status and let the client redirect to the list to reflect the change.

If the user is no longer in session, we will need to return `response['status'] = 403` for `Forbidden`, provide the appropriate `response['errorMsg'] = "Please login to access your list"` message, and `response['redirectUrl'] = "/login" will allow the client to redirect to login page.

We will refactor the function to use AJAX call in the front-end and handle the JSON response from the back-end. First, in our `templates/list.html`, we will remove the `action` and `method` attributes from the `add-new` form.

```
<form id="add-new">
    <div>
        <input type="text" id="new-list-item-text" name="text">
        <input type="submit" id="new-item-submit" value="Add" class="button">
    </div>
</form>
```

Then we modify the `static/js/list.js` file to make the AJAX call for sending the new item data:

```
$('#new-item-submit').click(function(e) {
    e.preventDefault();
    var text = $('#new-list-item-text').val();
    if (text) {
        var url = "/list/create";
        $.ajax({
            type: "POST",
            url: url,
            dataType: "json",
            data: {"text": text},
            success: function(response) {
                if (response) {
                    if (response.status != 201 && response.errorMsg) {
                        alert(response.errorMsg || "Create item failed");
                    }
                    if (response.redirectUrl) {
                        window.location.href = response.redirectUrl;
                    }
                }
            },
        });
    } else {
        alert("Item text should not be empty.");
    }
});
```

As with other AJAX calls, we will stop the default submit action by calling `e.preventDefault`, then `post` a request to `/list/create` with the `text` data. Upon success, we try to display any `errorMsg` and redirect to `redirectUrl` whenever available. If the `text` is empty, we will not attempt to send the request, but prompt an error message instead.

### Edit List Item

For edit function, it will be a little complicated due to a handful of validations to be done.

```
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
```

In our `handlers/list.py` file, we will change the `put` function to make use of the new list data structure. To make sure the request is genuine, we check that the `username` is in `self.get_secure_cookie("user")` and return `response['status'] = 403` if it is not. We also need to make sure the `text` is not empty, and will return `response['status'] = 400` if it is. Just in case the `list_id` is not found in `self.get_secure_cookie("list_id")`, we will return `response['status'] = 404` as well. Finally we will validate the `item_id` actually exists in the database by calling `list_items.find` with the `item_id`, and will return `response['status'] = 404` if no item is found. After all the various validations, we can finally call `list_items.update_one` and pass in the `{'$set':{'text':text}}` as the modification to apply. This will return `response['status'] = 200` to indicate `OK` status.

For `user` and `list_id` not found in `self.get_secure_cookie`, it means that the user is no longer logged in, and we should return `response['redirectUrl'] = "/login"` so that the client can redirect to the login page for user to re-login. Otherwise, we will just return `response['redirectUrl'] = "/list"` for the client to refresh the list page.

We also change our `static/js/list.js` file to handle the new RESTful JSON response from the server.

```
$('.edit-button').click(function() {
    var itemSpan = $(this).parent();
    var itemId = $(itemSpan).find("input[type='hidden']").val();
    var text = $(itemSpan).find("input[name='text']").val();
    if (text) {
        var url = "/list/" + itemId + "/edit";
        $.ajax({
            type: "PUT",
            url: url,
            dataType: "json",
            data: {"text": text},
            success: function(response) {
                if (response) {
                    if (response.status != 200 && response.errorMsg) {
                        alert(response.errorMsg || "Update item failed");
                    }
                    if (response.redirectUrl) {
                        window.location.href = response.redirectUrl;
                    }
                }
            },
        });
    } else {
        alert("Item text should not be empty.");
    }
});
```

We will check that the `text` field is not empty, then send a `PUT` request to `/list/<itemid>/edit` with `text` data. Upon success, we will display any `errorMsg` and redirect to `redirectUrl` whenever available.

### Delete List Item

The delete logic will be similar to the edit logic, except that instead of calling `list_items.update_one`, we will call `list_items.remove`.

```
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
```

There is no need to validate `text` input here. We just need to make sure the `user` and `list_id` are still in `self.get_secure_cookie`, and the `item_id` exists in the database, then we can `list_items.remove` the item.

Our `static/js/list.js` file will also be modified:

```
$('.delete-button').click(function() {
    var itemSpan = $(this).parent();
    var itemId = $(itemSpan).find("input[type='hidden']").val();
    var url = "/list/" + itemId + "/delete";
    $.ajax({
        type: "DELETE",
        url: url,
        dataType: "json",
        data: {},
        success: function(response) {
            if (response) {
                if (response.status != 200 && response.errorMsg) {
                    alert(response.errorMsg || "Delete item failed");
                }
                if (response.redirectUrl) {
                    window.location.href = response.redirectUrl;
                }
            }
        },
    });
});
```

You can see that it is similar in structure as the edit function, except that we don't need to pass the `text` field as data to the request.

[Back to top](#table-of-contents)

# Refactoring the App

So far our handler classes have been inheriting directly from `tornado.web.RequestHandler`. This means that all the handlers will use the default behaviour provided by the class, but sometimes we want to customize things to suit our needs. In this case, it is better to write a `BaseHandler` that inherits from `tornado.web.RequestHandler`, and override certain functions to customize the behaviour, then all our handlers will inherit from `BaseHandler` all the customized functions.

[Back to top](#table-of-contents)

## Base Handler

You might have noticed that we have a few places where we call `self.get_secure_cookie("user").decode("utf-8")` or `self.set_secure_cookie("user", user)`. It gets a little lengthy after a while. Also, if we somehow decide to add additional logic when getting the current user, we have to change all places using `self.get_secure_cookie("user").decode("utf-8")`. A better approach will be to override `get_current_user` of `tornado.web.RequestHandler` in our `BaseHandler`. On top of that, we also create some shortcut functions to get the current session information. 

First, we will create a new `handlers/base.py` file.

```
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
```

In this new file, we will create a `BaseHandler` class that extends `tornado.web.RequestHandler`. The class should be initialized with a `db` object. We will have functions that deal with session values.

`get_current_session` is created as a shortcut to retrieve current session's `user` and `list_id` in a tuple. This is so that we don't need to call `get_current_user` and `get_current_list` separately. Corresponding to getting the current session, we also have a convenient function to `set_current_session`. Sometimes, we need to clear session data at once, and it's easier to do it with `clear_current_session`.

However, sometimes we might just need either `user` or `list_id` from the session, so we still have individual `get_current_user` and `get_current_list` functions and their setter counterparts.

### `urls.py`

Since we are extending from `BaseHandler`, we need to always provide the `db` object to the class. We have to change `urls.py` accordingly for `MainHandler`.

```
url(r"/", MainHandler, dict(db=db)),
```

### `handlers/main.py`

We will show one example of how to change the handlers to extend `BaseHandler`.

```
from handlers.base import BaseHandler

class MainHandler(BaseHandler):
    def initialize(self, db):
        super().initialize(db)
```

For example, in our `handlers/main.py`, we will change the parent class of `MainHandler` to `BaseHandler`, and we call `super().initialize(db)` instead of directly setting `self.db = db` as previously done.

Besides, we also need to change all the `self.get_secure_cookie("user")` to `self.get_current_user()`.

The other handlers should follow the same style as in `main.py`:

1. Import base handler class by `from handlers.base import BaseHandler`
2. Extend `BaseHandler` and call `super().initialize(db)`
3. Change all `self.set_secure_cookie("user", username)` to `self.set_current_user(username)`
4. Change all `self.get_secure_cookie("user")` to `self.get_current_user()`
5. Change all `self.set_secure_cookie("list_id", list_id)` to `self.set_current_list(list_id)`
6. Change all `self.get_secure_cookie("list_id")` to `self.get_current_list()`

In places where we need both `user` and `list_id`, we can call the `username,list_id = self.get_current_session()` to get both values at once.

### `LogoutHandler`

```
def post(self):
    if self.get_current_user():
        self.clear_current_session()
```

In our `LogoutHandler`, we also change to use `self.clear_current_session` so that we don't have to call `self.set_current_user("")` and `self.set_current_list("")`.

[Back to top](#table-of-contents)

## Write Response

Other than session values, another function that we call frequently is `self.write`, and we pass in a `response` object with attributes such as `status` and `redirectUrl`. Instead of having to create the `response` object everytime we need to write a response, why not we provide a common function in the `BaseHandler` that takes in just the `status` and `redirectUrl`, and will take care of creating the `response` and `write` it?

```
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
```

Let's revisit the `BaseHandler` class. We will add a few more functions that deal with writing response. A base `write_response` function will take a required `status_code` argument, and a list of keyword arguments, then create a `response` object. By default it must set the `status` attribute, then if `redirectUrl` and `errorMsg` are found in the keyword arguments, they will be added to the `response` accordingly. Finally, it will call `json.dumps(response)` and `self.write` to write the response in JSON format.

We provide a few commonly used status response, such as `200`, `201`, `400`, `403` and `404`. These functions do not take the `status_code`, instead it is set accordingly based on the purpose of the function. For example, the `write_response_ok` function will set `200` when calling `write_response`, then the `**kwargs` will be passed to `write_response` as-is.

Except that for `write_response_forbidden`, we know that we want the user to login to access the resource, so we default the `redirectUrl` to `/login`.

### `account.py`

Let's look at an example of how to make use of the `BaseHandler`'s `write` functions.

```
if users.find_one({'username': username}):
    self.write_response_bad(errorMsg="User already exists", redirectUrl="/account/create")
```

In our `AccountHandler`, somewhere in the `post` function we have the code to `self.write(json.dumps(response))`. We can now replace this with just `self.write_response_bad(errorMsg="Useralready exists", redirectUrl="/account/create")`.

The rest of our handlers will follow the same pattern, calling the respective `write_response` according to status and passing the `errorMsg` and `redirectUrl` keyword arguments when necessary.

[Back to top](#table-of-contents)
  
## Error Handling

So far we have been seeing a plain text error message page that prints all the stack trace to the user. We don't actually want users to see the internals of our application, instead, we should customize a pretty page that gracefully shows an error message about the error.

To achieve that, we will need to override `write_error` function of `tornado.web.RequestHandler`, and create a custom `error.html` template to display the error message. 

Besides, we should also provide a custom `404.html` page that is displayed when the user request for a resource that does not exist.

### `BaseHandler`

```
def write_error(self, status_code, **kwargs):
    if 'exc_info' in kwargs:
        err_cls, err, traceback = kwargs['exc_info']
    errorMsg = err if err else ""
    self.render("error.html", code=status_code, message=errorMsg)
```

In our `BaseHandler`, we will override `write_error` function. In the [official docs](http://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler.write_error), it is mentioned that if the `write_error` is caused by an uncaught exception, a `exc_info` tuple will be available in `kwargs`. This tuple contains the error class, the error message and the stack trace of the error. For our error page, we only need to output the simple error message, so we will take the 2nd value in the tuple and return as `message` for rendering. 

Then we create the `templates/error.html` to display the error message.

```
{% extends "base.html" %}
{% block content %}
<div class="alert alert-danger" role="alert">An error has occurred!{% if message %}<br>{{ message }}{% end %}</div>
{% end %}
```

### `ErrorHandler`

Another common type of error encountered will be the famous `404` error. Instead of showing the default `404` page, we will create a custom `404` page for rendering.

To render that custom page, we will need to create a custom `ErrorHandler` class in the `handlers/base.py` file.

```
class ErrorHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.render("404.html")
```

We override the `prepare` function, which will be called before `get` or `post`. This allows us to intercept the requests where the resource is not available, and then render a `404.html` page.

We need to tell our application to use this custom `ErrorHandler` class by a special setting in `settings.py`.

```
from handlers.base import ErrorHandler

### other codes omitted

settings['default_handler_class'] = ErrorHandler
```

Under `settings`, we will add one more attribute `default_handler_class` and assign `ErrorHandler` class to it.

Finally, we create `templates/404.html` that will display an error message when the user requests for a resource that does not exist.

```
{% extends "base.html" %}
{% block content %}
<div class="alert alert-danger" role="alert">Opps! The page you requested for has not been created. Go back to <a href="/">home</a> and try again.<div>
{% end %}
```

### `main.css`

Since we have created new classes for displaying error messages, we must not forget to add the style to our `main.css`.

```
.alert { padding: 20px; width: 400px; border-radius: 5px; }
.alert-danger { background-color: #e33; color: #eee; }
```

[Back to top](#table-of-contents)

