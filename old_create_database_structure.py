from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_database.db'
database = SQLAlchemy(application)


class Accounts(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    login = database.Column(database.String(80), unique=True, nullable=False)
    first_name = database.Column(database.String(80))
    last_name = database.Column(database.String(80))
    email = database.Column(database.String(80), unique=True, nullable=False)
    password = database.Column(database.String(80), nullable=False)
    total_rating = database.Column(database.Integer, nullable=False)
    registration_date = database.Column(database.DateTime, nullable=False)
    birthday = database.Column(database.Date)

    def __repr__(self):
        return f'{self.id}'


class Courses(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    link = database.Column(database.String(80), unique=True, nullable=False)
    logo_file_name = database.Column(database.String(80), unique=True, nullable=False)
    name = database.Column(database.String(80), unique=True, nullable=False)
    price = database.Column(database.Integer, nullable=False)
    description = database.Column(database.Text)
    lessons_number = database.Column(database.Integer, nullable=False)
    rating = database.Column(database.Integer)
    passage_time = database.Column(database.Integer)


class ActiveCourses(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    account_id = database.Column(database.Integer, database.ForeignKey('accounts.id'), nullable=False)
    account = database.relationship('Accounts', backref=database.backref('activecourses', lazy=False))
    course_id = database.Column(database.Integer, database.ForeignKey('courses.id'), nullable=False)
    course = database.relationship('Courses', backref=database.backref('activecourses', lazy=False))
    percentage_of_passing = database.Column(database.Integer, nullable=False)
    mark = database.Column(database.Float, nullable=False)


database.create_all()
