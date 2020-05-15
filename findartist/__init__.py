from flask import Flask
from config import Config, TestConfig


def create_app(testing=False):
    app = Flask(__name__)
    if testing:
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    from findartist.routes import main

    app.register_blueprint(main)

    return app

