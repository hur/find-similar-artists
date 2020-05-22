"""Defines fixtures available to all tests."""

import pytest
from rq import SimpleWorker

from findartist import create_app


@pytest.fixture
def app():
    """ Create application for the tests. """
    _app = create_app(testing=True)

    ctx = _app.test_request_context()
    ctx.push()
    yield _app
    ctx.pop()


@pytest.fixture
def client(app):
    """ Flask test client """
    return app.test_client()


@pytest.fixture(scope='function')
def worker(app):
    """ RQ test worker """
    _worker = SimpleWorker([app.task_queue], connection=app.redis)
    return _worker


def pytest_configure(config):
    """ Configuration for custom markers """
    config.addinivalue_line(
        "markers", "long: mark test as long running (deselect with '-m \"not long\"') "
    )
