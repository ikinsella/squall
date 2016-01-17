from flask import (Blueprint,
                   render_template,
                   flash,
                   request,
                   redirect,
                   url_for)
from flask.ext.login import login_required
from appname.extensions import cache
from appname.forms import BatchForm
from appname.models import (db,
                            Tag,
                            Experiment,
                            Implementation,
                            DataSet,
                            Batch)


batches = Blueprint('batches', __name__)


@batches.route('/')
@cache.cached(timeout=1000)
@login_required
def get_batch():
    batch_form = BatchForm()
    batch_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    batch_form.experiment.choices\
        = [(e.id, e.name) for e in Experiment.query.order_by('name')]
    batch_form.implementation.choices\
        = [(i.id, i.name) for i in Implementation.query.order_by('name')]
    batch_form.data_set.choices\
        = [(ds.id, ds.name) for ds in DataSet.query.order_by('name')]
    return render_template('batches.html',
                           batch_form=batch_form)


@batches.route('/save_batch', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_batch():
    batch_form = BatchForm()
    batch_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    batch_form.experiment.choices\
        = [(e.id, e.name) for e in Experiment.query.order_by('name')]
    batch_form.implementation.choices\
        = [(i.id, i.name) for i in Implementation.query.order_by('name')]
    batch_form.data_set.choices\
        = [(ds.id, ds.name) for ds in DataSet.query.order_by('name')]
    if batch_form.validate_on_submit():
        batch = Batch(batch_form.name.data,
                      batch_form.description.data,
                      batch_form.experiment.data,
                      batch_form.data_set.data,
                      batch_form.implementation.data)
        db.session.add(batch)
        db.session.commit()
        tag_ids = batch_form.tags.data
        batch.tags = [Tag.query.filter_by(id=tag).first() for tag in tag_ids]
        db.session.commit()
        flash("New batch added successfully", "success")
    else:
        flash('Failed validation', 'danger')

    return redirect(url_for("batches.get_batch"))
