from flask import (Blueprint,
                   render_template,
                   flash,
                   redirect,
                   url_for,
                   current_app,
                   send_from_directory)
from flask.ext.login import login_required
from appname.extensions import cache
from appname.forms import (BatchForm, DownloadBatchForm, UploadResultsForm)
from appname.models import (db,
                            mongo,
                            Tag,
                            Experiment,
                            Implementation,
                            DataSet,
                            Batch)
from appname.controllers.constants import (MEMORY,
                                           DISK,
                                           FLOCK,
                                           GLIDE)
from flask_table import (Table, Col)


batches = Blueprint('batches', __name__)


@batches.route('/')
@cache.cached(timeout=1000)
@login_required
def batch():
    """ """
    return render_template('batches.html',
                           batch_form=create_batch_form(),
                           download_form=create_download_form(),
                           results_form=create_results_form(),
                           batch_table=create_batch_table())


@batches.route('/submit_batch', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_batch():
    """ """
    batch_form = create_batch_form()
    if batch_form.validate_on_submit():
        db.session.add(Batch(
            experiment_id=batch_form.experiment.data,
            data_set_id=batch_form.data_set.data,
            implementation_id=batch_form.implementation.data,
            name=batch_form.name.data,
            description=batch_form.description.data,
            tags=[Tag.query.filter_by(id=_id).first()
                  for _id in batch_form.tags.data],
            params=batch_form.params.data,
            memory=batch_form.memory.data,
            disk=batch_form.disk.data,
            flock=batch_form.flock.data,
            glide=batch_form.glide.data))
        db.session.commit()
        flash("New batch added successfully", "success")
        return redirect(url_for("batches.batch"))
    flash("Failed validation", "danger")
    return render_template('batches.html',
                           batch_form=batch_form,
                           download_form=create_download_form(),
                           results_form=create_results_form(),
                           batch_table=create_batch_table())


@batches.route('/download_batch', methods=["Get", "Post"])
@cache.cached(timeout=1000)
@login_required
def download_batch():
    """ """
    download_form = create_download_form()
    if download_form.validate_on_submit():
        batch = Batch.query.filter_by(id=download_form.batch.data).first()
        flash("Download Started", "success")
        return send_from_directory(current_app.config['STAGING_AREA'],
                                   batch.package(),
                                   as_attachment=True)
    flash("Failed validation", "danger")
    return render_template('batches.html',
                           batch_form=create_batch_form(),
                           download_form=download_form,
                           results_form=create_results_form(),
                           batch_table=create_batch_table())


@batches.route('/upload_results', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def upload_results():
    """Add the results form a batch to MongoDB job by job"""
    results_form = create_results_form()
    if results_form.validate_on_submit():
        batch = Batch.query.filter_by(id=results_form.batch.data).first()
        col = mongo.db[Experiment.query.filter_by(
            id=batch.experiment_id).first().name]
        metadata = batch.mongoize
        for job in results_form.results.data:
            job.update(metadata)
            col.insert(job)  # Insert each job as a separate document
        batch.completed = True  # Update Batch Status In SQL
        db.session.add(batch)
        db.session.commit()
        flash("Results Stored In MongoDB", "success")
        return redirect(url_for("batches.batch"))
    flash("Upload Failed: Validation Error", "danger")
    return render_template('batches.html',
                           batch_form=create_batch_form(),
                           download_form=create_download_form(),
                           results_form=results_form,
                           batch_table=create_batch_table())


class BatchTable(Table):
    id = Col('Batch ID')
    name = Col('Batch Name')
    exp = Col('Experiment')
    set = Col('Data Set')
    imp = Col('Algorithm Implemention')
    mem = Col('Memory (MB)')
    disk = Col('Disk Space (KB)')
    flock = Col('Flock')
    glide = Col('Glide')
    descr = Col('Description')
    tags = Col('Tags')
    size = Col('Size')
    completed = Col('Completed')

    def tr_format(self, item):
        return '<tr valign="top">{}</tr>'


class BatchItem(Table):
    def __init__(self, id, name, exp, set, imp, mem, disk,
                 flock, glide, descr, tags, size, completed):
        self.name = name
        self.id = id
        self.exp = exp
        self.set = set
        self.imp = imp
        self.mem = mem
        self.disk = disk
        self.flock = flock
        self.glide = glide
        self.descr = descr
        self.tags = tags
        self.size = size
        self.completed = completed


def create_batch_table():
    """ """
    return BatchTable([BatchItem(
        batch.id,
        batch.name,
        Experiment.query.filter(
            Experiment.batches.any()).first().name,
        DataSet.query.filter(
            DataSet.batches.any()).first().name,
        Implementation.query.filter(
            Implementation.batches.any()).first().name,
        batch.memory,
        batch.disk,
        batch.flock,
        batch.glide,
        batch.description,
        '\n'.join([str(tag.name) for tag in
                   Tag.query.filter(Tag.batches.any(id=batch.id)).all()]),
        batch.size,
        batch.completed) for batch in Batch.query.all()])


def create_batch_form():
    """ """
    form = BatchForm(memory=MEMORY, disk=DISK, flock=FLOCK, glide=GLIDE)
    form.tags.choices = [(t.id, t.name) for t in Tag.query.order_by('_name')]
    form.experiment.choices = [(e.id, e.name) for e in
                               Experiment.query.order_by('_name')]
    form.implementation.choices = [(i.id, i.name) for i in
                                   Implementation.query.order_by('_name')]
    form.data_set.choices = [(ds.id, ds.name) for ds in
                             DataSet.query.order_by('_name')]
    return form


def create_download_form():
    """ """
    form = DownloadBatchForm()
    form.batch.choices = [(b.id, b.name) for b in
                          Batch.query.order_by('_name')]
    return form


def create_results_form():
    """ """
    form = UploadResultsForm()
    form.batch.choices = [(b.id, b.name) for b in
                          Batch.query.order_by('_name')]
    return form
