from flask import Blueprint, request, jsonify
from models import Order, TrackingStatus, PermitStatus
import random
import string
from middleware import tokenRequired

order = Blueprint("order", __name__)


# route to get all orders, must send token
@order.route("/all", methods=["GET"])
@tokenRequired
def getAll():
    if request.method == "GET":
        orders = Order.objects

        return jsonify(orders)


# route to create a new order, will mainly be called from Leap to Digital web hook, or from admin
@order.route("/newOrder", methods=["POST"])
def newOrder():
    if request.method == "POST":
        print("REQUEST ******************************************")
        print(request)
        print("REQUEST.FORM ***************************")
        print(request.form)
        print("REQUEST.FORM KEYS ***************************")
        print(request.form.keys())
        return {"stuff": "stuff"}, 200
        # customername = request.form["customerName"]
        # jobaddress = request.form["address"]
        # # create random 10 digit code
        # ordernumber = ''.join(random.choices(
        #     string.ascii_uppercase + string.digits, k=10))

        # while Order.objects(orderNumber=ordernumber):
        #     ordernumber = ''.join(random.choices(
        #         string.ascii_uppercase + string.digits, k=10))

        # neworder = Order(orderNumber=ordernumber,
        #                  customerName=customername, jobAddress=jobaddress).save()
        # return jsonify(neworder)

        # # how can i secure this to only being called from the leaptodigital webhook
        # return "only leap to digital web hook allowed to access this, create new post in db, send status back"


# retrieve specific order
@order.route("/<orderNum>", methods=["GET"])
def getOrder(orderNum):
    # send back the one specific order
    if request.method == "GET":
        order = Order.objects(orderNumber=orderNum)
        if not order:
            return {"err": "Could not find the order number " + orderNum}, 400
        else:
            return jsonify(order[0])


# delete specific order, token required
@order.route("/delete/<orderNum>", methods=["POST"])
@tokenRequired
def deleteOrder(orderNum):
    if request.method == "POST":
        order = Order.objects(orderNumber=orderNum)
        if not order:
            return {"err": "Could not find the order number " + orderNum + " for deletion"}
        else:
            order.delete()
            return {"success": orderNum + " successfully deleted"}, 200


# order to update tracking or permit status, by enum
@order.route("/update/<orderNum>", methods=["POST"])
@tokenRequired
def updateOrder(orderNum):
    order = Order.objects(orderNumber=orderNum)
    if not order:
        return {"err": "Could not find the order number" + orderNum + " for update"}, 400

    updated = False

    if "tracking" in request.form:
        if hasattr(TrackingStatus, request.form["tracking"]):
            order.update(trackingStatus=TrackingStatus[
                request.form["tracking"]].value)
            updated = True

    if "permit" in request.form:
        if hasattr(PermitStatus, request.form["permit"]):
            updated = True
            order.update(
                permitStatus=PermitStatus[request.form["permit"]].value)

    if "customerName" in request.form:
        updated = True
        order.update(customerName=request.form["customerName"])

    if "jobAddress" in request.form:
        updated = True
        order.update(jobAddress=request.form["jobAddress"])

    if updated:
        return {"success": "Order updated successfully"}, 200
    else:
        return {"err": "Nothing was updated, please check args"}, 400
