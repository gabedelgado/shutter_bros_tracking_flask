from middleware import tokenRequired
from flask import Blueprint, request
import jwt
from models import User
from dotenv import load_dotenv
import os
load_dotenv()

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
@tokenRequired
def signup():
    if request.method == "POST":
        username, password, password2 = request.form[
            "username"], request.form["password"], request.form["password2"]
        if password != password2:
            return "Passwords did not match.", 400
        user = User().signup(username, password)
        if not user:
            return "That username was already taken.", 400
        else:
            token = jwt.encode(
                {"user": str(user.id)}, os.environ.get("TOKEN_SECRET"), algorithm="HS256")
            return token


@auth.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username, password = request.form['username'], request.form['password']

        user = User().login(username, password)
        if not user:
            return {"err": "The username or password was incorrect"}, 401
        else:
            token = jwt.encode(
                {"user": str(user.id)}, os.environ.get("TOKEN_SECRET"), algorithm="HS256")
            return token


@auth.route("/verifytoken", methods=["POST"])
@tokenRequired
def verifytoken():
    return {"verified": "true"}, 200
