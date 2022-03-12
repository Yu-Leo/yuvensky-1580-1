from app.main import database
import hashlib
from typing import Optional
import datetime

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


def create_database_structure():
    database.create_all()
