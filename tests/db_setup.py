from neo4j import GraphDatabase
from flask import current_app, g
from flask.cli import with_appcontext

import time

def test_db():
	with get_db().session() as session:
		# create test note-rel->user
		session.run("CREATE (n:Note {title:'Note 1',body:'test note 1 for Alice',"
					" archive:'false', noteid:'Alice" + str(int(time.time()))+"'})-[r:belongsTo]->(a:User {name:'Alice'})")

		session.run("CREATE (n:Note {title:'Note 2',body:'test note 2 for Bob',"
					"archive:'false', noteid:'Bob" + str(int(time.time()))+"'})-[r:belongsTo]->(a:User {name:'Bob'})")
