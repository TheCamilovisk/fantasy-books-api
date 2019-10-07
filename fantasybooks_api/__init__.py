from flask import Flask
from flask_cors import CORS


def create_app(config=None):

    app = Flask(__name__)

    from .auth.resources import user_bp

    app.register_blueprint(user_bp)

    CORS(app)

    return app
