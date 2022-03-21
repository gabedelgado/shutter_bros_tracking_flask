from flask import Blueprint

testpage = Blueprint("/test",  __name__)


@testpage.route("/")
def homeapi():
    return "test to /test successful"


@testpage.route("/otherthings")
def otherthings():
    return "test to other things"
