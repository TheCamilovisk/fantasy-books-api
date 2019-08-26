from flask import Flask, jsonify


def create_app(config=None):

    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return jsonify({'msg': 'Hello, World!!!!'})

    return app
