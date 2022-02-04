import flask
from Course import Course

application = flask.Flask(__name__)


@application.errorhandler(404)
def page_not_found(e):
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


def get_courses():
    c1 = Course("python_basics", "python_logo.jpg", "Python. Основы", 0, "Супер курс!")
    c2 = Course("python_basics", "python_logo.jpg", "Python. Pro", 2000, "Супер курс!")
    c3 = Course("python_basics", "cpp_logo.png", "C++. Основы", 0, "Супер курс!")
    c4 = Course("python_basics", "cpp_logo.png", "C++. Pro", 3000, "Супер курс!")
    return [c1, c2, c3, c4]


@application.route('/courses')
def courses():
    return flask.render_template("courses.html", courses=get_courses())


@application.route('/python_basics')
def python_basics():
    return flask.render_template("python_basics.html")


if __name__ == '__main__':
    application.run(debug=True)
