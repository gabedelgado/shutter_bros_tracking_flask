from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("localhost", 27017)


@app.route('/')
def home():
    return "hi there"


if __name__ == "__main__":
    app.run()
