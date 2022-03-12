import flask
from flask_sqlalchemy import SQLAlchemy

application = flask.Flask(__name__)
application.config.from_object("config")
database = SQLAlchemy(application)
