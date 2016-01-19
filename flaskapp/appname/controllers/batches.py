from flask import (Blueprint,
                   render_template,
                   flash,
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
from appname.controllers.constants import (MEMORY,
                                           DISK,
                                           FLOCK,
                                           GLIDE)
import yaml

batches = Blueprint('batches', __name__)


@batches.route('/')
@cache.cached(timeout=1000)
@login_required
def batch():
    batch_form = BatchForm(memory=MEMORY, disk=DISK, flock=FLOCK, glide=GLIDE)
    batch_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('_name')]
    batch_form.experiment.choices\
        = [(e.id, e.name) for e in Experiment.query.order_by('_name')]
    batch_form.implementation.choices\
        = [(i.id, i.name) for i in Implementation.query.order_by('_name')]
    batch_form.data_set.choices\
        = [(ds.id, ds.name) for ds in DataSet.query.order_by('_name')]
    return render_template('batches.html', batch_form=batch_form)


@batches.route('/submit_batch', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_batch():
    batch_form = BatchForm(memory=MEMORY, disk=DISK, flock=FLOCK, glide=GLIDE)
    batch_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('_name')]
    batch_form.experiment.choices\
        = [(e.id, e.name) for e in Experiment.query.order_by('_name')]
    batch_form.implementation.choices\
        = [(i.id, i.name) for i in Implementation.query.order_by('_name')]
    batch_form.data_set.choices\
        = [(ds.id, ds.name) for ds in DataSet.query.order_by('_name')]
    if batch_form.validate_on_submit():  # TODO: Validate File Loading
        tags = [Tag.query.filter_by(id=_id).first()
                for _id in batch_form.tags.data]
        batch = Batch(experiment_id=batch_form.experiment.data,
                      data_set_id=batch_form.data_set.data,
                      implementation_id=batch_form.implementation.data,
                      name=batch_form.name.data,
                      description=batch_form.description.data,
                      tags=tags,
                      params=yaml.load(batch_form.params.data),
                      memory=batch_form.memory.data,
                      disk=batch_form.disk.data,
                      flock=batch_form.flock.data,
                      glide=batch_form.glide.data)
        db.session.add(batch)
        db.session.commit()
        flash("New batch added successfully", "success")
        return redirect(url_for("batches.batch"))
    flash("Failed validation", "danger")
    return render_template('batches.html', batch_form=batch_form)
