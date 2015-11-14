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
                            Algorithm,
                            experiments_tags,
                            Experiment,
                            collections_experiments,
                            algorithms_experiments,
                            data_sets_experiments)


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
    experiment_form = ExperimentForm()
    experiment_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    experiment_form.collections.choices\
        = [(collection.id, collection.name) for collection in DataCollection.query.order_by('name')]
    experiment_form.algorithms.choices\
        = [(algorithm.id, algorithm.name) for algorithm in Algorithm.query.order_by('name')]
    if experiment_form.validate_on_submit():
        new_experiment = Experiment(experiment_form.name.data, experiment_form.description.data)
        db.session.add(new_experiment)
        db.session.commit()

        # store experiment collections
        selected_collections = experiment_form.collections.data
        for collection in selected_collections:
            new_collection = DataCollection.query.filter_by(id=collection).first()
            new_experiment.collections.append(new_collection)
            db.session.commit()

        # store experiment algorithms
        selected_algorithms = experiment_form.algorithms.data
        for algorithm in selected_algorithms:
            new_algorithm = Algorithm.query.filter_by(id=algorithm).first()
            new_experiment.algorithms.append(new_algorithm)
            db.session.commit()

        # store experiment tags
        experiment_tag_id = Experiment.get_id(new_experiment)
        selected_tags = experiment_form.tags.data
        for tag in selected_tags:
            new_tag = Tag.query.filter_by(id=tag).first()
            new_experiment.tags.append(new_tag)
            db.session.commit()

        flash("New experiment added successfully.", "success")
    return redirect(url_for("experiments.get_experiment"))
