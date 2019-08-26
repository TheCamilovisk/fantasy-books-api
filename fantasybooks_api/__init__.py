from flask import Flask


def create_app(config=None):

    app = Flask(__name__)

    from .auth.resources import user_bp

    app.register_blueprint(user_bp)

    return app
