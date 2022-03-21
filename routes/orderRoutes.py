from flask import Blueprint, request

order = Blueprint("order", __name__)


@order.route("/all")
def getAll():
    # send back all the orders stored from db
    # need to authenticate with jwt from admin
    if request.method == "GET":
        return "get all orders"


@order.route("/<orderNum>")
def getOrder(orderNum):
    # send back the one specific order
    # no need to authenticate right ?? think about this
    if request.method == "GET":
        return "get the order" + orderNum


# FIND OUT WHY THIS DOESNT WORK
@order.route("/newOrder")
def newOrder():
    if request.method == "POST":
        # how can i secure this to only being called from the leaptodigital webhook
        return "i will create new order here"


@order.route("/delete/<orderNum>")
def deleteOrder(orderNum):
    if request.method == "POST":
        # add jwt verify here !!!!
        return "i will delete the order " + orderNum + " here"
