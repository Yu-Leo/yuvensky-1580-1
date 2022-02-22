import datetime
import os
import flask
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from typing import Optional

DATABASE_FILE_NAME = "database.db"

application = flask.Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_FILE_NAME}"
database = SQLAlchemy(application)
application.secret_key = "secret"


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

    def validate(self, password):
        print("comp:", self.password, password)
        return self.password == password
        # return self.password == hashlib.md5(password.encode("utf8")).hexdigest()


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
    account_id = database.Column(database.Integer, database.ForeignKey("accounts.id"), nullable=False)
    account = database.relationship("Accounts", backref=database.backref("activecourses", lazy=False))
    course_id = database.Column(database.Integer, database.ForeignKey("courses.id"), nullable=False)
    course = database.relationship("Courses", backref=database.backref("activecourses", lazy=False))
    percentage_of_passing = database.Column(database.Integer, nullable=False)
    mark = database.Column(database.Float, nullable=False)


class Reviews(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80), nullable=False)
    email = database.Column(database.String(80), nullable=False)
    text = database.Column(database.Text)


def create_database_structure():
    database.create_all()


def add_courses():
    course_python_basics = Courses(link="python_basics",
                                   logo_file_name="python_logo.jpg",
                                   name="Python. Основы",
                                   price=0,
                                   description="Курс по основам Python 3",
                                   lessons_number=5,
                                   rating=100,
                                   passage_time=15)

    course_python_pro = Courses(link="python_pro",
                                logo_file_name="python_logo.jpg",
                                name="Python. Pro",
                                price=3000,
                                description="Супер курс с профессиональными фишками Python ",
                                lessons_number=5,
                                rating=200,
                                passage_time=30)

    course_cpp_basics = Courses(link="cpp_basics",
                                logo_file_name="cpp_logo.png",
                                name="C++. Основы",
                                price=0,
                                description="Курс по основам C++",
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


def add_reviews():
    review_1 = Reviews(name="Иван",
                       email="vanya@gmail.com",
                       text="Отличный сайт!")

    review_2 = Reviews(name="Антон",
                       email="anton@yandex.ru",
                       text="Курсы супер!")

    database.session.add(review_1)
    database.session.add(review_2)
    database.session.commit()


def add_accounts():
    leo = Accounts(
        login="leo",
        first_name="Leo",
        last_name="Yu",
        email="l@gmail.com",
        password="12345",
        total_rating=100,
        registration_date=datetime.datetime.now(),
        birthday=datetime.datetime.now())
    database.session.add(leo)
    database.session.commit()


def get_courses(min_price: Optional[str], max_price: Optional[str]) -> list:
    all_courses = Courses.query.all()
    if min_price is not None and max_price is not None:
        filtered = list(filter(lambda course: int(min_price) <= course.price <= int(max_price), all_courses))
    elif min_price is not None and max_price is None:
        filtered = list(filter(lambda course: int(min_price) <= course.price, all_courses))
    elif min_price is None and max_price is not None:
        filtered = list(filter(lambda course: course.price <= int(max_price), all_courses))
    else:
        filtered = all_courses
    return filtered


def get_course_by_link(link: str):
    all_courses: list = Courses.query.all()
    filtered = list(filter(lambda course: course.link == link, all_courses))
    return filtered[0] if len(filtered) == 1 else None


def get_reviews() -> list:
    return Reviews.query.all()[::-1]


def does_database_file_exist() -> bool:
    return os.path.isfile(DATABASE_FILE_NAME)


@application.errorhandler(404)
def page_not_found(error):
    return flask.render_template("404.html"), 404


@application.route("/")
def main_page():
    return flask.render_template("index.html")


@application.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        login = flask.request.form.get("login")
        password = flask.request.form.get("password")
        try:
            if Accounts.query.filter_by(login=login).one().validate(password):
                flask.session["login"] = login
                flask.flash(f"Welcome back, {login}", "success")
                return flask.redirect(flask.url_for("main_page"), code=301)
            flask.flash("Wrong login or password", "warning")
        except sqlalchemy.exc.NoResultFound:
            flask.flash("Wrong login or password", "danger")

    return flask.render_template("login.html")


@application.route("/logout")
def logout():
    if flask.session.get("login"):
        flask.session.pop("login")
    return flask.redirect("/", code=302)


@application.route("/about_us")
def about_us():
    return flask.render_template("about_us.html")


@application.route("/reviews", methods=["GET", "POST"])
def reviews():
    if flask.request.method == "POST":
        name = flask.request.form.get("name")
        email = flask.request.form.get("email")
        text = flask.request.form.get("text")
        if name != "" and email != "" and text != "":
            review = Reviews(name=name,
                             email=email,
                             text=text)
            database.session.add(review)
            database.session.commit()
    return flask.render_template("reviews.html", reviews=get_reviews())


@application.route("/404")
def null_page():
    return flask.render_template("404.html")


@application.route("/courses")
def courses():
    min_price = flask.request.args.get("min_price", None)
    max_price = flask.request.args.get("max_price", None)
    return flask.render_template("courses.html", courses=get_courses(min_price, max_price))


@application.route("/course/<course>")
def show_course_page(course):
    return flask.render_template("course_page.html", course=get_course_by_link(course))


if __name__ == "__main__":
    if not does_database_file_exist():
        create_database_structure()
        add_courses()
        add_reviews()
        add_accounts()
    application.run(debug=True)
