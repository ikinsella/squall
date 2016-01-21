from flask import (Blueprint,
                   render_template,
                   flash, request,
                   redirect,
                   url_for)
from flask.ext.login import (login_user,
                             logout_user,
                             login_required)

from appname.extensions import cache
from appname.forms import LoginForm, CreateUserForm
from appname.models import db, User

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route("/login", methods=["GET", "POST"])
def login():
    # if g.user is not None and g.user.is_authenticated:
        #  return redirect(url_for('restricted'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)
        flash("Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for(".home"))
    flash("Failed validation", "danger")
    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for(".home"))


@main.route("/restricted", methods=["Get", "Post"])
@login_required
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(form.username.data,
                    form.launch_directory.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("New user created successfully.", "success")
        return redirect(url_for(".home"))
    flash("Failed validation", "danger")
    return render_template("create_user.html", form=form)
