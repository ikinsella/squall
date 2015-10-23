from flask import (Blueprint,
                   render_template,
                   flash,
                   request,
                   redirect,
                   url_for)
from flask.ext.login import login_required
from appname.extensions import cache
from appname.forms import TagForm
from appname.models import db


tags = Blueprint('tags', __name__)


@tags.route('/')
@cache.cached(timeout=1000)
@login_required
def get_tag():
    tag_form = TagForm()
    return render_template('tags.html',
                           tag_form=tag_form)


@tags.route('/save_tag', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_tag():
    flash("The Tag Will Have Been Saved")
    return redirect(url_for("tags.get_tag"))
