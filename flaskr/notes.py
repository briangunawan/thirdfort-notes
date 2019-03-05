import functools
import requests

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.exceptions import abort


from flaskr.auth import login_required
from flaskr.db import get_notes, get_note, create_note, delete_note, update_note, get_archived_notes

bp = Blueprint('notes', __name__, url_prefix='/notes')

# Endpoint to view notes created by user and create a new note.
@bp.route('/', methods=(['GET', 'POST']))
@login_required
def index():
	if request.method == 'GET':

		notes = get_notes(session['username'])	
		print(notes)
		return render_template('notes/index.html', notes=notes)

	elif request.method == 'POST':

		create_note(session['username'], request.form['title'], request.form['body'])
		return redirect('/')

# endpoint to view archived notes
@bp.route('/archived', methods=(['GET']))
@login_required
def archived():
	if request.method == 'GET':

		notes = get_archived_notes(session['username'])
		print(notes)
		return render_template('notes/index.html', notes=notes)

# Endpoints regarding a specific note.
# GET: view note by ID
# DELETE: delete note
# PUT: update information of a note
@bp.route('/<id>', methods=(['GET', 'DELETE', 'PUT']))
@login_required
def view_note(id):
	print('view', id)
	if request.method == 'GET':
		note = get_note(id)
		if note is not None:
			return render_template('notes/note.html', note=note)
		else:
			return redirect('/')

	elif request.method == 'DELETE':
		print('deleting')
		delete_note(id)
		note = get_note(id)
		if note is not None:
			return render_template('notes/note.html', note=note)
		else:
			return redirect('/')

	elif request.method == 'PUT':
		print(id, request.data, request.form)
		update_note(id, request.form['title'], request.form['body'], request.form['archived'])
		return redirect('/' + id)



	return redirect('/')

# Front end helper endpoints as html5 does not implement sending DELETE and PUT requests 
@bp.route('/<id>/delete', methods=(['GET','POST']))
@login_required
def delete(id):
	return requests.delete(request.url_root + 'notes/{}'.format(id)).content


@bp.route('/new', methods=(['GET']))
@login_required
def new():
	return render_template('notes/new.html')

