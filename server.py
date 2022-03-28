from flask import Flask, request
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from models import User
from routes.orderRoutes import order
from routes.authRoutes import auth
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)
# separate routes into different blueprints
app.register_blueprint(order, url_prefix="/api/order")
app.register_blueprint(auth, url_prefix="/api/auth")

# Connecting to mongodb
client = MongoClient("localhost", 27017)
app.config['MONGODB_SETTINGS'] = {
    'db': 'shutterBrosTracking',
    'host': 'localhost',
    'port': 27017
}

# setup mongoengine for easier access/manipulation of mongo db
db = MongoEngine(app)

if __name__ == "__main__":
    app.run()
