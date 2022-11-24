import os
import json

from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

from .settings import (
    MONGO_USER, MONGO_PASS, MONGO_DATABASE, MONGO_PORT, MONGO_HOST)


# create and configure the app
app = Flask(__name__)

# configure mongodb settings
app.config['MONGODB_SETTINGS'] = {
    'db': MONGO_DATABASE,
    'host': MONGO_HOST,
    'port': int(MONGO_PORT),
    'username': MONGO_USER,
    'password': MONGO_PASS
}
db = MongoEngine()
db.init_app(app)


try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# register blueprint
from . import order
app.register_blueprint(order.bp)

# registering init-db custom script
from .db import init_app
init_app(app)

if __name__ == "__main__":
    app.run()