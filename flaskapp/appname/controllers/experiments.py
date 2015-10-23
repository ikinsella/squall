from flask import (Blueprint,
                   render_template,
                   flash,
                   request,
                   redirect,
                   url_for)
from flask.ext.login import login_required
from appname.extensions import cache
from appname.forms import ExperimentForm
from appname.models import (db,
                            Tag,
                            DataCollection,
                            Algorithm)


experiments = Blueprint('experiments', __name__)


@experiments.route('/')
@cache.cached(timeout=1000)
@login_required
def get_experiment():
    experiment_form = ExperimentForm()
    experiment_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    experiment_form.algorithms.choices\
        = [(a.id, a.name) for a in Algorithm.query.order_by('name')]
    experiment_form.collections.choices\
        = [(dc.id, dc.name) for dc in DataCollection.query.order_by('name')]
    return render_template('experiments.html',
                           experiment_form=experiment_form)


@experiments.route('/save_experiment', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_experiment():
    flash("The Experiment Will Have Been Saved")
    return redirect(url_for("experiments.get_experiment"))
