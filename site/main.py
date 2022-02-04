import os
import flask
from flask_sqlalchemy import SQLAlchemy

DATABASE_FILE_NAME = "database.db"

application = flask.Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_FILE_NAME}'
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


class Courses(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    link = database.Column(database.String(80), nullable=False)
    logo_file_name = database.Column(database.String(80), nullable=False)
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


def create_database_structure():
    database.create_all()


def add_courses():
    course_python_basics = Courses(link="python_basics",
                                   logo_file_name="python_logo.jpg",
                                   name="Python. Основы",
                                   price=0,
                                   description="Супер курс по основам Python",
                                   lessons_number=5,
                                   rating=100,
                                   passage_time=15)

    course_python_pro = Courses(link="python_pro",
                                logo_file_name="python_logo.jpg",
                                name="Python. Pro",
                                price=5000,
                                description="Супер курс с профессиональными фишками Python ",
                                lessons_number=5,
                                rating=200,
                                passage_time=30)

    course_cpp_basics = Courses(link="cpp_basics",
                                logo_file_name="cpp_logo.png",
                                name="C++. Основы",
                                price=0,
                                description="Супер курс по основам C++",
                                lessons_number=5,
                                rating=200,
                                passage_time=30)

    course_cpp_pro = Courses(link="cpp_pro",
                             logo_file_name="cpp_logo.png",
                             name="C++. Pro",
                             price=5000,
                             description="Супер курс с профессиональными фишками C++",
                             lessons_number=5,
                             rating=200,
                             passage_time=30)

    database.session.add(course_python_basics)
    database.session.add(course_python_pro)
    database.session.add(course_cpp_basics)
    database.session.add(course_cpp_pro)
    database.session.commit()


def does_database_file_exist() -> bool:
    return os.path.isfile(DATABASE_FILE_NAME)


@application.errorhandler(404)
def page_not_found(error):
    return flask.render_template('404.html'), 404


@application.route('/index')
def main_page():
    return flask.render_template("index.html")


@application.route('/about_us')
def about_us():
    return flask.render_template("about_us.html")


@application.route('/reviews')
def reviews():
    return flask.render_template("reviews.html")


@application.route('/404')
def null_page():
    return flask.render_template("404.html")


def get_courses() -> list:
    return Courses.query.all()


@application.route('/courses')
def courses():
    return flask.render_template("courses.html", courses=get_courses())


@application.route('/python_basics')
def python_basics():
    return flask.render_template("python_basics.html")


if __name__ == '__main__':
    if not does_database_file_exist():
        create_database_structure()
        add_courses()
    application.run(debug=True)
