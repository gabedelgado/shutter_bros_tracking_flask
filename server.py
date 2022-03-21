from flask import Flask, request
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from models import User
from moreRoutes import testpage
from routes.orderRoutes import order

app = Flask(__name__)

# separate routes into different files like this, add url prefix like this.
app.register_blueprint(testpage, url_prefix="/test")
app.register_blueprint(order, url_prefix="/api/order")
# connect to mongodb like this
client = MongoClient("localhost", 27017)
app.config['MONGODB_SETTINGS'] = {
    'db': 'testflaskdb',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine(app)


@app.route('/<stuff>/<otherstuff>', methods=["GET", "POST"])
def home(stuff, otherstuff):  # for normal url params do like this line and line above, and use as normal variable

    if request.method == "GET":

        # print(request.ars)
        print(otherstuff)
        return stuff

    if request.method == "POST":
        # for post form submission use request.form
        print(request.form['username'])
        print(request.form['password'])
        return "you did a post"


@app.route('/', methods=["GET"])
def otherhome():
    if request.method == "GET":
        User(name='laura', email='poop@gmail.com').save()
        # print(request.args["arg"])  # for query params use request.args
        return "i print"


if __name__ == "__main__":
    app.run()
