from flask import Blueprint, request
import jwt
from models import User

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        if User().signup(username, password):
            return "signed up " + username
        else:
            return "something went wrong when trying to sign you up"
        return "will sign you up here, check username does not exist in db, create new jwt token and send back"


@auth.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username, password = request.form['username'], request.form['password']
        return User().login(username, password)
