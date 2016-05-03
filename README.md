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
    <li class="{{ item["color"] }}">
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
    <li class="{{ item["color"] }}">
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
settings["debug"] = options.debug
settings["static_path"] = STATIC_ROOT
settings["template_path"] = TEMPLATE_ROOT
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

