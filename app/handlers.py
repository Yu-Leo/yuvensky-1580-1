import sqlalchemy
from app.models import *
from app.main import application, database
import flask


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
