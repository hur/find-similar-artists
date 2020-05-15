"""Defines fixtures available to all tests."""

import pytest
from findartist import create_app


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app(testing=True)

    ctx = _app.test_request_context()
    ctx.push()
    yield _app
    ctx.pop()


@pytest.fixture
def client(app, db):
    """Flask test client"""
    return app.test_client()
