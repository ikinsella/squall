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
from flask_table import (Table, Col)


experiments = Blueprint('experiments', __name__)


@experiments.route('/')
@cache.cached(timeout=1000)
@login_required
def experiment():
    """ """
    return render_template('experiments.html',
                           experiment_form=create_experiment_form(),
                           exp_table=create_experiment_table())


@experiments.route('/submit_experiment', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_experiment():
    experiment_form = create_experiment_form()
    if experiment_form.validate_on_submit():
        db.session.add(Experiment(
            name=experiment_form.name.data,
            description=experiment_form.description.data,
            tags=[Tag.query.filter_by(id=_id).first()
                  for _id in experiment_form.tags.data],
            algorithms=[Algorithm.query.filter_by(id=_id).first()
                        for _id in experiment_form.algorithms.data],
            collections=[DataCollection.query.filter_by(id=_id).first()
                         for _id in experiment_form.collections.data]))
        db.session.commit()
        flash("New experiment added successfully.", "success")
        return redirect(url_for("experiments.experiment"))
    flash('Failed validation', 'danger')
    return render_template('experiments.html',
                           experiment_form=experiment_form,
                           exp_table=create_experiment_table)


class ExpTable(Table):
    id = Col('Experiment ID')
    name = Col('Experiment Name')
    collections = Col('Data Collections')
    algorithms = Col('Algorithms')
    description = Col('Description')
    tags = Col('Tags')

    def tr_format(self, item):
        return '<tr valign="top">{}</tr>'


class ExpItem(object):
    def __init__(self, id, name, collections, algorithms, description, tags):
        self.name = name
        self.id = id
        self.collections = collections
        self.algorithms = algorithms
        self.description = description
        self.tags = tags


def create_experiment_table():
    """ """
    return ExpTable([ExpItem(
        exp.id,
        exp.name,
        '\n'.join([str(coll.name) for coll in DataCollection.query.filter(
            DataCollection.experiments.any(id=exp.id)).all()]),
        '\n'.join([str(alg.name) for alg in Algorithm.query.filter(
            Algorithm.experiments.any(id=exp.id)).all()]),
        exp.description,
        '\n'.join([tag.name for tag in Tag.query.filter(Tag.experiments.any(
            id=exp.id)).all()])) for exp in Experiment.query.all()])


def create_experiment_form():
    """ """
    form = ExperimentForm()
    form.tags.choices = [(t.id, t.name) for t in
                         Tag.query.order_by('_name')]
    form.algorithms.choices = [(a.id, a.name) for a in
                               Algorithm.query.order_by('_name')]
    form.collections.choices = [(dc.id, dc.name) for dc in
                                DataCollection.query.order_by('_name')]
    return form
