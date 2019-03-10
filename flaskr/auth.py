import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db, default_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

# login endpoint. Currently takes any username and adds it to the db if new.
# To extend: add password field. Hash and salt when adding to db for security.
# Create sign up page. Did not spend too much time here as it was not part of the task.
@bp.route('/login', methods=(['GET','POST']))
def login():
    if request.method == 'POST':
        username = request.form['username']
        # add password in further development

        db = get_db()
        error = None

        if not username:
        	error = 'Username Required'

        default_user(username)
        session.clear()
        session['username'] = username
        return redirect(url_for('index'))

    else:
        return "please log in"

# log the user out
@bp.route('/logout', methods=(['GET']))
def logout():
    session.clear()
    return redirect(url_for('index'))

# load logged in user before each request
@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = username

# require auth in other views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view