import os
import json

from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'your_database',
        'host': 'localhost',
        'port': 27017
    }
    db = MongoEngine()
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    class User(db.Document):
        name = db.StringField()
        email = db.StringField()

        def to_json(self):
            return {"name": self.name,
                    "email": self.email}

    @app.route('/', methods=['GET'])
    def query_records():
        name = request.args.get('name')
        user = User.objects(name=name).first()
        if not user:
            return jsonify({'error': 'data not found'})
        else:
            return jsonify(user.to_json())

    @app.route('/', methods=['PUT'])
    def create_record():
        record = json.loads(request.data)
        user = User(name=record['name'],
                    email=record['email'])
        user.save()
        return jsonify(user.to_json())

    @app.route('/', methods=['POST'])
    def update_record():
        record = json.loads(request.data)
        user = User.objects(name=record['name']).first()
        if not user:
            return jsonify({'error': 'data not found'})
        else:
            user.update(email=record['email'])
        return jsonify(user.to_json())

    @app.route('/', methods=['DELETE'])
    def delete_record():
        record = json.loads(request.data)
        user = User.objects(name=record['name']).first()
        if not user:
            return jsonify({'error': 'data not found'})
        else:
            user.delete()
        return jsonify(user.to_json())

    return app
