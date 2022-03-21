from enum import Enum
from mongoengine import Document, StringField, EnumField


class User(Document):
    name = StringField()
    email = StringField()


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
