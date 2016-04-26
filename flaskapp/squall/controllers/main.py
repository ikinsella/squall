from flask import (Blueprint,
                   render_template,
                   flash, request,
                   redirect,
                   url_for, json, jsonify)
from flask.ext.login import (login_user,
                             logout_user,
                             login_required, current_user)

from squall.extensions import cache
from squall.forms import LoginForm, CreateUserForm, UserViewForm, EditUserForm
from squall.models import db, User
from werkzeug.security import generate_password_hash

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


@main.route("/restricted")
@login_required
def create_user():
    return render_template("create_user.html", form=CreateUserForm(),
                           display_all_form=create_view_form(),
                           edit_form=create_edit_form())

@main.route("/create_user", methods=["Get", "Post"])
@login_required
def add_user():
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
    return render_template("create_user.html", form=form,
                           display_all_form=create_view_form(),
                           edit_form=create_edit_form())


@main.route("/edit_user", methods=["GET", "POST"])
@login_required
def edit_user():
    edit_form = create_edit_form()
    curr_user = User.query.filter_by(id=current_user.get_id()).first()
    if edit_form.validate_on_submit():
        curr_user.password = generate_password_hash(edit_form.edit_pw.data)
        db.session.commit()
        curr_user.launch_directory = edit_form.edit_dir.data
        db.session.commit()
        flash("User information updated", "success")
        return redirect(url_for(".home"))

    flash("Failed validation", "danger")
    return render_template("create_user.html", form=CreateUserForm(),
                           display_all_form=create_view_form(),
                           edit_form=edit_form)


@main.route('/select_user', methods=['POST', 'GET'])
def select_user():
    userid = json.loads(request.form.get('data'))['userid']
    return jsonify({'name': User.query.filter(
        User.id == userid).first().username, 'dir': User.query.filter(
            User.id == userid).first()._launch_directory})


def create_view_form():
    display_all_form = UserViewForm()
    display_all_form.users.choices = [(0, 'Select User')] + [
        (u.id, u.username) for u in User.query.order_by('username')]
    return display_all_form


def create_edit_form():
    edit_form = EditUserForm()
    edit_form.edit_username.data = User.query.filter_by(
        id=current_user.get_id()).first().username
    return edit_form
