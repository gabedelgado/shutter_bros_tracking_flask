from enum import Enum
from mongoengine import Document, StringField, EnumField
from bcrypt import gensalt, hashpw, checkpw
import jwt
from dotenv import load_dotenv
import os

load_dotenv()


class User(Document):
    username = StringField()
    password = StringField()

    def login(self, username, password):
        user = User.objects(username=username)
        print(os.environ.get("TOKEN_SECRET"))
        if not user:
            return "couldnt find anyone with that username"
        elif (not checkpw(password.encode("utf-8"), user[0].password.encode("utf-8"))):
            return "the passwords did not match"
        else:
            token = jwt.encode(
                {"user": str(user[0].id)}, os.environ.get("TOKEN_SECRET"), algorithm="HS256")
            return token

    def signup(self, username, password):
        if User.objects(username=username):
            return "this username was already taken"
        else:
            salt = gensalt()
            hashedpass = hashpw(password.encode("utf-8"), salt)
            user = User(username=username, password=hashedpass).save()
            token = jwt.encode(
                {"user": str(user.id)}, os.environ.get("TOKEN_SECRET"), algorithm="HS256")
            return token


class TrackingStatus(Enum):
    PENDING = "Pending"
    FINALMEASUREMENTSTAKEN = "Final Measurements Taken"
    ORDERPLACED = "Order Placed"
    PRODUCTSBEINGFABRICATED = "Products being Fabricated"
    ORDERSHIPPED = "Order Shipped to Shutter Brothers"
    ORDERRECEIVED = "Order Received at Shutter Brothers"
    QUALITYCONTROLINSPECTION = "Quality Control Inspection"
    READYTOINSTALL = "Products Ready to be Installed"
    INSTALLATIONCOMPLETE = "Installaion Complete"


class PermitStatus(Enum):
    PENDING = "Pending"
    DOCUMENTSSIGNED = "Documents Signed"
    SUBMITTED = "Submitted"
    COUNTYREVIEW = "County Review"
    REVISIONS = "Revisions"
    PERMITISSUED = "Permit Issued"


class Order(Document):
    orderNumber = StringField(required=True, unique=True)
    customerName = StringField(required=True)
    jobAddress = StringField(required=True)
    trackingStatus = EnumField(TrackingStatus, default=TrackingStatus.PENDING)
    permitStatus = EnumField(PermitStatus, default=PermitStatus.PENDING)
