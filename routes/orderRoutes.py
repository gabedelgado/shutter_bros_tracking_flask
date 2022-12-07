from flask import Blueprint, request, jsonify
from models import Order, TrackingStatus, PermitStatus
import random
import string
from middleware import tokenRequired
from twilio.rest import Client
import os
from dotenv import load_dotenv


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
        customerdata = request.get_json()["customer"]
        customername = customerdata["firstName"] + \
            " " + customerdata["lastName"]
        jobaddress = "%s, %s, %s %s" % (
            customerdata["street"], customerdata["city"], customerdata["state"], customerdata["zipCode"])
        customernumber = customerdata["phoneNumbers"][0]["number"]
        customeremail = customerdata["emails"][0]["email"]

        # # create random 10 digit code
        ordernumber = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))

        while Order.objects(orderNumber=ordernumber):
            ordernumber = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=10))

        neworder = Order(orderNumber=ordernumber,
                         customerName=customername, jobAddress=jobaddress, phoneNumber=customernumber, email=customeremail, textUpdates=True, emailUpdates=False).save()
        return jsonify(neworder)

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

    if "customerName" in request.form:
        updated = True
        order.update(customerName=request.form["customerName"])

    if "jobAddress" in request.form:
        updated = True
        order.update(jobAddress=request.form["jobAddress"])

    if "email" in request.form:
        updated = True
        order.update(email=request.form["email"])

    if "phoneNumber" in request.form:
        updated = True
        order.update(phoneNumber=request.form["phoneNumber"])

    if "textUpdates" in request.form:
        updateValue = None
        if request.form["textUpdates"].lower() == "false":
            updateValue = False
        else:
            updateValue = True

        if updateValue is not None:
            order.update(textUpdates=updateValue)
            updated = True

    if "emailUpdates" in request.form:
        updateValue = None
        if request.form["textUpdates"].lower() == "false":
            updateValue = False
        else:
            updateValue = True

        if updateValue is not None:
            order.update(emailUpdates=updateValue)
            updated = True

    if "tracking" in request.form:
        if hasattr(TrackingStatus, request.form["tracking"]):

            if order[0].trackingStatus.value != TrackingStatus[
                    request.form["tracking"]].value and order[0].textUpdates == True:
                load_dotenv()
                account = os.environ.get("TWILIO_ACCOUNT")
                token = os.environ.get("TWILIO_TOKEN")
                client = Client(account, token)
                message = "This is a Shutter Brothers Tracking update for order " + orderNum + ". Your tracking status has been updated to " + TrackingStatus[
                    request.form["tracking"]].value.upper() + ". To view your order status online, please visit https://shutterbrotherstracking.netlify.app/order/" + orderNum
                toNumber = "+1" + order[0].phoneNumber.replace("-", "")
                client.messages.create(
                    to=toNumber, from_="+16406008901", body=message)

            order.update(trackingStatus=TrackingStatus[
                request.form["tracking"]].value)
            updated = True

    if "permit" in request.form:
        if hasattr(PermitStatus, request.form["permit"]):

            if order[0].permitStatus.value != PermitStatus[
                    request.form["permit"]].value and order[0].textUpdates == True:
                load_dotenv()
                account = os.environ.get("TWILIO_ACCOUNT")
                token = os.environ.get("TWILIO_TOKEN")
                client = Client(account, token)
                message = "This is a Shutter Brothers Tracking update for order " + orderNum + ". Your permit status has been updated to " + PermitStatus[
                    request.form["permit"]].value.upper() + ". To view your permit status online, please visit https://shutterbrotherstracking.netlify.app/order/" + orderNum
                toNumber = "+1" + order[0].phoneNumber.replace("-", "")
                client.messages.create(
                    to=toNumber, from_="+16406008901", body=message)

            updated = True
            order.update(
                permitStatus=PermitStatus[request.form["permit"]].value)

    if updated:
        return {"success": "Order updated successfully"}, 200
    else:
        return {"err": "Nothing was updated, please check args"}, 400
