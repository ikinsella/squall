from flask import (Blueprint,
                   render_template,
                   flash,
                   request,
                   redirect,
                   url_for)
from flask.ext.login import login_required
from appname.extensions import cache
from appname.forms import (AlgorithmForm,
                           ImplementationForm)
from appname.models import (db, Tag)


algorithms = Blueprint('algorithms', __name__)


@algorithms.route('/')
@cache.cached(timeout=1000)
@login_required
def get_algorithm():
    algorithm_form = AlgorithmForm()
    algorithm_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    implementation_form = ImplementationForm()
    implementation_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    return render_template('algorithms.html',
                           algorithm_form=algorithm_form,
                           implementation_form=implementation_form)


@algorithms.route('/save_algorithm', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_algorithm():
    flash("The Algorithm Will Have Been Saved")
    return redirect(url_for("algs.get_algorithm"))


@algorithms.route('/save_implementation', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_implementation():
    flash("The Implementation Will Have Been Saved")
    return redirect(url_for("algs.get_algorithm"))
