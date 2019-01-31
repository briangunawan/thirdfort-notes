import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.exceptions import abort

from flaskr.db import get_db

from flaskr.auth import login_required
from flaskr.db import get_db, get_notes

bp = Blueprint('notes', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
	db = get_db()

	notes = get_notes(session['username'])
	print(notes)
	return render_template('notes/index.html', notes=notes)


# @bp.route('/archived', methods=('GET', 'POST'))
# def index():
# 	db = get_db()

# 	notes = get_notes(session['username'])
# 	print(notes)
# 	return render_template('notes/index.html', notes=notes)
