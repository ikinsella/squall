from flask import (Blueprint,
                   render_template,
                   flash,
                   redirect,
                   url_for)
from flask.ext.login import login_required
from appname.extensions import cache
from appname.forms import ExperimentForm
from appname.models import (db,
                            Tag,
                            DataCollection,
                            Algorithm,
                            Experiment)


experiments = Blueprint('experiments', __name__)


@experiments.route('/')
@cache.cached(timeout=1000)
@login_required
def experiment():
    experiment_form = ExperimentForm()
    experiment_form.tags.choices\
        = [(t.id, t.name) for t in Tag.query.order_by('_name')]
    experiment_form.algorithms.choices\
        = [(a.id, a.name) for a in Algorithm.query.order_by('_name')]
    experiment_form.collections.choices\
        = [(dc.id, dc.name) for dc in DataCollection.query.order_by('_name')]
    return render_template('experiments.html',
                           experiment_form=experiment_form)


@experiments.route('/submit_experiment', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_experiment():
    experiment_form = ExperimentForm()
    experiment_form.tags.choices\
        = [(t.id, t.name) for t in Tag.query.order_by('_name')]
    experiment_form.collections.choices\
        = [(dc.id, dc.name) for dc in DataCollection.query.order_by('_name')]
    experiment_form.algorithms.choices\
        = [(a.id, a.name) for a in Algorithm.query.order_by('_name')]
    if experiment_form.validate_on_submit():
        tags = [Tag.query.filter_by(id=_id).first()
                for _id in experiment_form.tags.data]
        algorithms = [Algorithm.query.filter_by(id=_id).first()
                      for _id in experiment_form.algorithms.data]
        collections = [DataCollection.query.filter_by(id=_id).first()
                       for _id in experiment_form.collections.data]
        experiment = Experiment(name=experiment_form.name.data,
                                description=experiment_form.description.data,
                                tags=tags,
                                algorithms=algorithms,
                                collections=collections)
        db.session.add(experiment)
        db.session.commit()
        flash("New experiment added successfully.", "success")
        return redirect(url_for("experiments.experiment"))
    flash('Failed validation', 'danger')
    return render_template('experiments.html',
                           experiment_form=experiment_form)
