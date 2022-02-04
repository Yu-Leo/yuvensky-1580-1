import flask

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


@application.route('/courses')
def courses():
    return flask.render_template("courses.html")


@application.route('/python_basics')
def python_basics():
    return flask.render_template("python_basics.html")


if __name__ == '__main__':
    application.run(debug=True)
