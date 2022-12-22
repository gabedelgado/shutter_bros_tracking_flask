from flask import Flask
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from routes.orderRoutes import order
from routes.authRoutes import auth
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
cors = CORS(app)

# separate routes into different blueprints
app.register_blueprint(order, url_prefix="/api/order")
app.register_blueprint(auth, url_prefix="/api/auth")

# Connecting to mongodb

# *** production ***
client = MongoClient(host=os.environ.get("MONGO_URI"), connect=False)

# *** development ***
# client = MongoClient(connect=False)

# *** production ***
app.config['MONGODB_SETTINGS'] = {
    'db': 'shutterBrosTracking',
    'host': os.environ.get("MONGO_URI"),
    'connect': False
}

# *** development ***
# app.config['MONGODB_SETTINGS'] = {
#     'db': 'shutterBrosTracking',
#     'host': 'localhost',
#     'port': 27017,
#     'connect': False
# }

# setup mongoengine for easier access/manipulation of mongo db
db = MongoEngine(app)

if __name__ == "__main__":
    app.run(port=10000)
