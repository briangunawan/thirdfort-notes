import pytest
from flaskr.db import get_db


def test_index(client, auth):
    response = client.get('http://localhost/notes/')
    assert b"login" in response.data

    auth.login()
    response = client.get('http://localhost/notes/')
    assert b'Log Out' in response.data
    assert b'Notes' in response.data
    assert b'Archived Notes' in response.data

    assert b'Note 2' in response.data
    assert b'test note 2 for Bob' in response.data

def test_archived(client, auth):
    auth.login()
    response = client.get('http://localhost/notes/archived', follow_redirects=True)

    assert b'Note 3' in response.data

@pytest.mark.parametrize('path', (
    'http://localhost/notes/',
    # '/archived',
    # '/notes/new'
))

def test_login_required(client, path):
    response = client.get('/', follow_redirects=True)
    assert b'Log In' in response.data


def test_new(client, auth, app):
    auth.login()
    assert client.get('notes/new').status_code == 200
    client.post('/notes/', data={'title': 'created title', 'body': 'created body'})

    with app.app_context():
        db = get_db()
        with db.session() as session:
            count = len(session.run("match (n:Note)-[r:belongsTo]->(u:User {name:'Bob'}) return n").data())
        assert count == 3


def test_update(client, auth, app):
    auth.login()
    with app.app_context():

        db = get_db()
        with db.session() as session:
            note = session.run("match (n:Note)-[r:belongsTo]->(u:User {name:'Bob'}) return n").data()[0]['n']
            print(note['noteid'])

            assert client.get('/notes/{}'.format(note['noteid'])).status_code == 200
            client.put('/notes/{}'.format(note['noteid']), data={'archived': 'false','title': 'updated title', 'body': ''})

            newNote = session.run("match (n:Note {{noteid: '{}'}}) return n".format(note['noteid'])).data()[0]['n']
            assert newNote['title'] == 'updated title'


def test_delete(client, auth, app):
    auth.login()
    with app.app_context():

        db = get_db()
        with db.session() as session:
            note = session.run("match (n:Note)-[r:belongsTo]->(u:User {name:'Bob'}) return n").data()[0]['n']
            count = len(session.run("match (n:Note)-[r:belongsTo]->(u:User {name:'Bob'}) return n").data())
            assert count == 2
            assert client.get('/notes/{}'.format(note['noteid'])).status_code == 200
            client.delete('/notes/{}'.format(note['noteid']))

            count = len(session.run("match (n:Note)-[r:belongsTo]->(u:User {name:'Bob'}) return n").data())
        assert count == 1
