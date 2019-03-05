from neo4j import GraphDatabase
from flask import current_app, g
from flask.cli import with_appcontext

import time

'''
This module contains the functions that set up the connection and communicates 
with the database.

'''

# Login function. Checks if name exist, if not add it as a new node.
def default_user(username):
	get_db()
	with g.db.session() as session:
		session.run("MERGE (u:User {{name:'{}'}})".format(username))

# get note by id
def get_note(noteid):
	get_db()
	with g.db.session() as session:
		ret = session.run("MATCH (n:Note {{noteid:'{}'}}) return n limit 1". format(noteid))
	ret = ret.single()
	print(ret)
	if ret is None:
		print('Noned')
		return None
	else:
		return ret[0]

# get non-archived notes
def get_notes(username):
	get_db()
	print('get', username)
	with g.db.session() as session:
		notes = session.run("match (u:User {{name:'{}'}})<-[r:belongsTo]-(n:Note) where n.archive='false' return n".format(username))
	print("match (u:User {{name:'{}'}})-[r:belongsTo]-(n:Note) where n.archive='false' return n".format(username))
	return [x['n'] for x in notes.data()]

# get archived notes
def get_archived_notes(username):
	get_db()
	with g.db.session() as session:
		notes = session.run("match (u:User {{name:'{}'}})<-[r:belongsTo]-(n:Note) where n.archive ='true' return n".format(username))
	# print(notes.data()[0]['n']['title'])
	return [x['n'] for x in notes.data()]

# create new note
def create_note(username, title, body):
	get_db()
	# add try, except and assert title/description
	noteid = username + str(int(time.time()))

	with g.db.session() as session:

		session.run("MATCH (u:User {{name:'{}'}}) \
			CREATE (n:Note {{title: '{}', body:'{}', archive:'false', noteid:'{}'}})-[:belongsTo]->(u)".format(username, title, body, noteid))

	return noteid

# update a note
def update_note(noteid, title, body, archived):
	get_db()
	print('udpating', title, body, archived)
	with g.db.session() as session:
		session.run("MATCH (n:Note {{noteid:'{}'}}) SET n.title='{}', n.body='{}', n.archive='{}'".format(noteid, title, body, archived))
	return 1

# delete a note
def delete_note(noteid):
	get_db()
	with g.db.session() as session:
		session.run("MATCH (n:Note {{noteid:'{}'}}) DETACH DELETE n".format(noteid))

	return 1

# function that creates and returns the connection to the db
def get_db():
	if 'db' not in g:
		g.db = GraphDatabase.driver('bolt://34.224.17.116:39272/', auth=('neo4j', 'north-blink-abilities'))
	return g.db


def init_app(app):
	app.teardown_appcontext(close_db)

# initialising function. Gets the db and adds it to the session global variable for
# later use. 
def init_db():
	print('init')
	db = get_db()
	
	# refreshes and adds mock data to the database. For dev use. Comment out as needed.
	test_db()



# refreshes the database and adds mock data for development and testing use.
def test_db():

	with get_db().session() as session:

		#delete existing data in graph
		session.run("MATCH (n) DETACH DELETE n")

		# add schema
		session.run("CREATE CONSTRAINT ON (u:User) ASSERT u.name IS UNIQUE")
		session.run("CREATE CONSTRAINT ON (n:Note) ASSERT n.noteid IS UNIQUE")

		# add test cases
		# create test note-rel->user
		session.run("CREATE (n:Note {title:'Note 1',body:'test note 1 for Alice',"
					" archive:'false', noteid:'Alice" + str(int(time.time()))+"'})-[r:belongsTo]->(a:User {name:'Alice'})")

		session.run("merge (n:Note {title:'Note 3',body:'test note 3 for Bob',"
					" archive:'true', noteid:'Bob" + str(int(time.time())+1)+"'})-[r:belongsTo]->(a:User {name:'Bob'})")

		session.run("match (a:User {name:'Bob'}) create (n:Note {title:'Note 2',body:'test note 2 for Bob',"
					"archive:'false', noteid:'Bob" + str(int(time.time()))+"'})-[r:belongsTo]->(a)")

# close the connection
def close_db(e=None):
    db = g.pop('db', None)