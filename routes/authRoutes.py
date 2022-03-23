from flask import Blueprint, request
import jwt
from models import User

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]
        return User().signup(username, password)


@auth.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username, password = request.form['username'], request.form['password']
        return User().login(username, password)
