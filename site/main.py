import datetime
import os
import flask
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from typing import Optional
import hashlib

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
        return self.password == hashlib.md5(password.encode("utf8")).hexdigest()

    def set_password(self, password):
        self.password = hashlib.md5(password.encode('utf8')).hexdigest()


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


class Cart(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    account_id = database.Column(database.Integer, database.ForeignKey("accounts.id"), nullable=False)
    account = database.relationship("Accounts", backref=database.backref("cart", lazy=False))
    course_id = database.Column(database.Integer, database.ForeignKey("courses.id"), nullable=False)
    course = database.relationship("Courses", backref=database.backref("cart", lazy=False))
    status = database.Column(database.Boolean, nullable=False)

    def set_not_active(self):
        self.status = False


class Reviews(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80), nullable=False)
    email = database.Column(database.String(80), nullable=False)
    text = database.Column(database.Text)


def create_database_structure():
    database.create_all()


def add_courses():
    course_python_basics = Courses(link="python_basic",
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
        password="None",
        total_rating=100,
        registration_date=datetime.datetime.now(),
        birthday=datetime.datetime.now())
    leo.set_password("leo")
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


def get_course_by_id(id: int):
    all_courses: list = Courses.query.all()
    filtered = list(filter(lambda course: course.id == id, all_courses))
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
                flask.flash(f"Добро пожаловать, {login}!", "success")
                return flask.redirect(flask.url_for("main_page"), code=301)
            flask.flash("Неправильный пароль", "warning")
        except sqlalchemy.exc.NoResultFound:
            flask.flash("Неправильный логин", "danger")

    return flask.render_template("login.html")


@application.route("/logout")
def logout():
    if flask.session.get("login"):
        flask.session.pop("login")
    return flask.redirect("/", code=302)


@application.route('/<login>', methods=['GET', 'POST'])
def profile(login):
    if flask.session.get('login') == login:
        if (Accounts.query.filter_by(login=login)) is not None:
            user = Accounts.query.filter_by(login=login)
            user = user.one()
            if flask.request.method == 'POST':
                old = flask.request.form.get('old_password')
                new = flask.request.form.get('new_password')

                if old == new == None:
                    flask.flash('Курсы куплены!', 'success')

                    cart_courses = get_active_cart_for_user(user.id)
                    for cc in cart_courses:
                        cc.set_not_active()
                        ac = ActiveCourses(account_id=user.id,
                                           course_id=cc.course_id,
                                           percentage_of_passing=0,
                                           mark=0)
                        database.session.add(ac)
                        database.session.add(cc)
                        database.session.commit()
                else:
                    if old == new:
                        flask.flash('Новый пароль тот же, что и старый', 'warning')
                    elif user.validate(old):
                        user.set_password(new)
                        flask.flash('Пароль изменен', 'success')
                        database.session.add(user)
                        database.session.commit()

            return flask.render_template('profile.html',
                                         user=user,
                                         cart=get_cart_for_user(user.id),
                                         active_courses=get_active_courses_for_user(user.id))

    flask.flash('Пожалуйста, войдите в свой аккаунт, чтобы продолжить', 'warning')
    return flask.redirect(flask.url_for('login'), code=301)


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


def check_course_in_cart(user_id, course_id):
    all_active_course = Cart.query.all()
    for ac in all_active_course:
        if ac.account_id == user_id and ac.course_id == course_id:
            return True
    return False


def get_active_courses_for_user(user_id):
    result = []
    all_active_course = ActiveCourses.query.all()
    for ac in all_active_course:
        if ac.account_id == user_id:
            result.append(get_course_by_id(ac.course_id))
    return result


def get_active_cart_for_user(user_id):
    result = []
    all_cart = Cart.query.all()
    for c in all_cart:
        if c.account_id == user_id and c.status:
            result.append(c)
    return result


def get_cart_for_user(user_id):
    result = []
    all_cart = Cart.query.all()
    for c in all_cart:
        if c.account_id == user_id and c.status:
            result.append(get_course_by_id(c.course_id))
    return result


@application.route("/course/<course>", methods=['GET', 'POST'])
def show_course_page(course):
    if flask.request.method == 'POST':
        if flask.session.get('login') is not None:
            user = Accounts.query.filter_by(login=flask.session.get('login'))
            if (user) is not None:
                user = user.one()
                if check_course_in_cart(user.id, get_course_by_link(course).id):
                    flask.flash('Курс уже куплен или находится в корзине', 'warning')
                else:

                    item = Cart(account_id=user.id,
                                course_id=get_course_by_link(course).id,
                                status=True)

                    database.session.add(item)
                    database.session.commit()

                    flask.flash('Курс добавлен в корзину', 'success')
                return flask.render_template("course_page.html", course=get_course_by_link(course))

        flask.flash('Пожалуйста, войдите в свой аккаунт, чтобы продолжить', 'warning')

    return flask.render_template("course_page.html", course=get_course_by_link(course))


if __name__ == "__main__":
    if not does_database_file_exist():
        create_database_structure()
        add_courses()
        add_reviews()
        add_accounts()
    application.run(debug=True)
