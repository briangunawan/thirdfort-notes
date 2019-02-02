import pytest
from flask import g, session
from flaskr.db import get_db


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/notes'

    with client:
        client.get('/')
        assert g.user == 'Bob'


# @pytest.mark.parametrize(('username', 'message'), (
#     ('a', 'test', b'Incorrect username.'),
#     ('test', 'a', b'Incorrect password.'),
# ))

# def test_login_validate_input(auth, username, password, message):
#     response = auth.login(username, password)
#     assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'username' not in session