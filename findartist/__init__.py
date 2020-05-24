import redis
from fakeredis import FakeStrictRedis
from flask import Flask
from config import Config, TestConfig
from rq import Queue


def create_app(testing: bool = False) -> object:
    """
    The application factory function.
    @param testing: boolean representing whether to use the testing configuration
    @return: an instance of the Flask class (the Flask application)
    """
    app = Flask(__name__)
    if testing:
        app.config.from_object(TestConfig)
        app.redis = FakeStrictRedis()
        app.task_queue = Queue(connection=app.redis)
    else:
        app.config.from_object(Config)
        app.redis = redis.from_url(app.config['REDIS_URL'])
        app.task_queue = Queue(connection=app.redis)

    from findartist.routes import main

    app.register_blueprint(main)

    return app

