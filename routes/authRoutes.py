from middleware import tokenRequired
from flask import Blueprint, request
import jwt
from models import User
from dotenv import load_dotenv
import os
load_dotenv()

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        user = User().signup(username, password)
        if not user:
            return {"err": "That username was already taken"}, 401
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
