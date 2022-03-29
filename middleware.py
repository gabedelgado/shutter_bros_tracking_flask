import os
import jwt
from flask import request
from functools import wraps
from dotenv import load_dotenv


# JWT authorization for certain routes
def tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        load_dotenv()
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            try:
                userid = jwt.decode(
                    token, os.environ.get("TOKEN_SECRET"), algorithms=["HS256"])
                # print(userid["user"])
            except Exception as e:
                return {"err": str(e)}, 401
        else:
            return {"err": "No token found !"}, 401

        return f(*args, **kwargs)
    return decorated
