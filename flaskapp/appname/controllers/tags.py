from flask import (Blueprint,
                   render_template,
                   flash,
                   redirect,
                   url_for)
from flask.ext.login import login_required
from appname.extensions import cache
from appname.forms import TagForm
from appname.models import db, Tag


tags = Blueprint('tags', __name__)


@tags.route('/')
@cache.cached(timeout=1000)
@login_required
def tag():
    tag_form = TagForm()
    return render_template('tags.html',
                           tag_form=tag_form)


@tags.route('/submit_tag', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_tag():
    tag_form = TagForm()
    if tag_form.validate_on_submit():
        new_tag = Tag(tag_form.name.data)
        db.session.add(new_tag)
        db.session.commit()
        flash("Tag added successfully.", "success")
        return redirect(url_for("tags.tag"))
    flash("Failed validation", "danger")
    return render_template('tags.html',
                           tag_form=tag_form)
