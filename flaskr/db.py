from py2neo import Graph, Node, Relationship, Schema, NodeMatcher, RelationshipMatcher, Subgraph

from flask import current_app, g
from flask.cli import with_appcontext

import time


def default_user(username):
	user = g.nmatcher.match('User', name=username).first()

	# if user doesn't exist, create user
	if user is None:
		g.db.create(Node('User',name=username))

# get non-archived notes
def get_notes(username):
	user = g.nmatcher.match('User', name=username).first()
	notes = [g.db.evaluate("match (u:User {{name:'{}'}})-[r:belongsTo]-(n:Note) where n.archive = False return n".format(username))]
	print(notes[0]['desc'])
	return list(notes)

# get archived notes
def get_archived_notes(username):
	user = g.nmatcher.match('User', name=username).first()
	notes = [g.db.evaluate("match (u:User {name:'Bob'})-[r:belongsTo]-(n:Note) where n.archive = True return n")]
	return list(notes)




def get_db():
	if 'db' not in g:
		# authenticate(current_app.config['DB_host_port'], current_app.config['DB_username'], current_app.config['DBpassword'])
		g.db = Graph('http://52.23.245.35:35356/', auth=('neo4j', 'rotations-grinders-advances'))
		g.nmatcher = NodeMatcher(g.db)
		g.rmatcher = RelationshipMatcher(g.db)
	return g.db


def init_app(app):
	app.teardown_appcontext(close_db)

def init_db():
	print('init')
	db = get_db()

# for dev: delete existing data in graph
	db.delete_all()

# add schema
	db.schema = create_schema()

	# add test cases
	test_db()

# create and return the schema for the graph
def create_schema():
	if 'db' in g:
		s = Schema(g.db)

	# s.create_index('User', 'name')
	s.create_index('Note', 'id')
	s.create_uniqueness_constraint('User','name')
	s.create_uniqueness_constraint('belongsTo','name')


	return s


def test_db():
	alice = Node("User", name="Alice")
	bob = Node("User", name="Bob")
	err = Node("User", name="Bob")

	n1 = Node('Note', desc='test note 1 for alice', archive=False, id=time.time())
	n2 = Node('Note', desc='test note 2 for bob', archive=False, id=time.time())
	an = Relationship(n1, 'belongsTo', alice)
	bn = Relationship(n2, 'belongsTo', bob)


	g.db.create(alice)
	g.db.create(bob)
	# g.db.create(err)

	g.db.create(n1)
	g.db.create(n2)
	g.db.create(an)
	g.db.create(bn)



def close_db(e=None):
    db = g.pop('db', None)