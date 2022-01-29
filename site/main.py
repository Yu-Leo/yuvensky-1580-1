import flask

application = flask.Flask(__name__)


@application.route('/index')
def main_page():
    return flask.render_template("index.html")


@application.route('/about_us')
def about_us():
    return flask.render_template("about_us.html")


@application.route('/reviews')
def reviews():
    return flask.render_template("reviews.html")


@application.route('/null_page')
def null_page():
    return flask.render_template("null_page.html")


@application.route('/courses')
def courses():
    return flask.render_template("courses.html")


@application.route('/python_basics')
def python_basics():
    return flask.render_template("python_basics.html")


if __name__ == '__main__':
    application.run(debug=True)
