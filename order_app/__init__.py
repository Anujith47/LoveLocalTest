import os
import json

from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine


# create and configure the app
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'lovedb',
    'host': 'mongo',
    'port': 27017,
    'username': 'root',
    'password': 'pass'
}
db = MongoEngine()
db.init_app(app)


try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from . import order
app.register_blueprint(order.bp)


from .db import init_app
init_app(app)

if __name__ == "__main__":
    app.run()