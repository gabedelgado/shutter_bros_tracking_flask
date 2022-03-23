from lib2to3.pgen2 import token
from flask import Blueprint, request
from functools import wraps

order = Blueprint("order", __name__)

# create jwt authentication like this, look at trello for good example


def tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return f("extra stuff", *args, **kwargs)
    return decorated


@order.route("/all")
@tokenRequired
def getAll(extras):
    # send back all the orders stored from db
    # need to authenticate with jwt from admin
    if request.method == "GET":
        print(extras)
        return "get all orders from db and send back in json form"


@order.route("/newOrder", methods=["POST"])
def newOrder():
    if request.method == "POST":
        # how can i secure this to only being called from the leaptodigital webhook
        return "only leap to digital web hook allowed to access this, create new post in db, send status back"


@order.route("/<orderNum>", methods=["GET"])
def getOrder(orderNum):
    # send back the one specific order
    # no need to authenticate right ?? think about this
    if request.method == "GET":
        return "get the order" + orderNum + " and send back in json form"


@order.route("/delete/<orderNum>", methods=["POST"])
def deleteOrder(orderNum):
    if request.method == "POST":
        # add jwt verify here !!!!
        return "i will delete the order " + orderNum + " from the db and return a response"
