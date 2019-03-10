import os

from flask import Flask, redirect, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # import modules
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import notes
    app.register_blueprint(notes.bp)
    app.add_url_rule('/notes', endpoint='index')

    from . import api
    app.register_blueprint(api.bp)
    app.add_url_rule('/api/notes', endpoint='api')


    # end point to refresh the database with mock data
    @app.route('/refresh')
    def hello():
        db.init_db()
        return 'Database refreshed'


    @app.route('/')
    def reroute():
        return redirect(url_for('index'))



    return app
