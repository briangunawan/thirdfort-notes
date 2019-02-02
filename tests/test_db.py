import neo4j

import pytest
from flaskr.db import get_db


def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

