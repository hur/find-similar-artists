import redis
from flask import Flask
from config import Config, TestConfig
from rq import Queue


def create_app(testing=False):
    app = Flask(__name__)
    if testing:
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    app.redis = redis.from_url(app.config['REDIS_URL'])
    app.task_queue = Queue(connection=app.redis)

    from findartist.routes import main

    app.register_blueprint(main)

    return app

