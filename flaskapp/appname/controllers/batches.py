import json
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
from flask_table import Table, Col

batches = Blueprint('batches', __name__)


@batches.route('/')
@cache.cached(timeout=1000)
@login_required
def batch():
    
    all_batches = Batch.query.all()
    batch_items = []
    for batch in all_batches:
        b_id = batch.id
        b_name = batch.name
        b_descr = batch.description
        b_mem = batch.memory
        b_disk = batch.disk
        b_flock = batch.flock
        b_glide = batch.glide
        b_descr = batch.description
        b_tags = [tag.name for tag in Tag.query.filter(Tag.batches.any(id=b_id)).all()]
        b_exp = Experiment.query.filter(Experiment.batches.any()).first().name
        b_set = DataSet.query.filter(DataSet.batches.any()).first().name
        b_imp = Implementation.query.filter(Implementation.batches.any()).first().name
        b_size = batch.size
        b_completed = batch.completed
        batch_items.append(BatchItem(b_id, b_name, b_exp, b_set, b_imp, b_mem, b_disk, b_flock, b_glide, b_descr, '\n'.join([str(x) for x in b_tags]), b_size, b_completed))
    batch_table = BatchTable(batch_items)

    
    batch_form = BatchForm(memory=MEMORY, disk=DISK, flock=FLOCK, glide=GLIDE)
    batch_form.tags.choices = [(t.id, t.name) for t in
                               Tag.query.order_by('_name')]
    batch_form.experiment.choices = [(e.id, e.name) for e in
                                     Experiment.query.order_by('_name')]
    batch_form.implementation.choices = [(i.id, i.name) for i in
                                         Implementation.query.order_by('_name')]
    batch_form.data_set.choices = [(ds.id, ds.name) for ds in
                                   DataSet.query.order_by('_name')]
    download_form = DownloadBatchForm()
    download_form.batch.choices = [(b.id, b.name) for b in
                                   Batch.query.order_by('_name')]
    results_form = UploadResultsForm()
    results_form.batch.choices = [(b.id, b.name) for b in
                                  Batch.query.order_by('_name')]
    return render_template('batches.html',
                           batch_form=batch_form,
                           download_form=download_form,
                           results_form=results_form,
                           batch_table=batch_table)


@batches.route('/submit_batch', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_batch():
    
    all_batches = Batch.query.all()
    batch_items = []
    for batch in all_batches:
        b_id = batch.id
        b_name = batch.name
        b_descr = batch.description
        b_mem = batch.memory
        b_disk = batch.disk
        b_flock = batch.flock
        b_glide = batch.glide
        b_descr = batch.description
        b_tags = [tag.name for tag in Tag.query.filter(Tag.batches.any(id=b_id)).all()]
        b_exp = Experiment.query.filter(Experiment.batches.any()).first().name
        b_set = DataSet.query.filter(DataSet.batches.any()).first().name
        b_imp = Implementation.query.filter(Implementation.batches.any()).first().name
        b_size = batch.size
        b_completed = batch.completed
        batch_items.append(BatchItem(b_id, b_name, b_exp, b_set, b_imp, b_mem, b_disk, b_flock, b_glide, b_descr, '\n'.join([str(x) for x in b_tags]), b_size, b_completed))
    batch_table = BatchTable(batch_items)

    batch_form = BatchForm(memory=MEMORY, disk=DISK, flock=FLOCK, glide=GLIDE)
    batch_form.tags.choices = [(t.id, t.name) for t in
                               Tag.query.order_by('_name')]
    batch_form.experiment.choices = [(e.id, e.name) for e in
                                     Experiment.query.order_by('_name')]
    batch_form.implementation.choices = [(i.id, i.name) for i in
                                         Implementation.query.order_by('_name')]
    batch_form.data_set.choices = [(ds.id, ds.name) for ds in
                                   DataSet.query.order_by('_name')]
    download_form = DownloadBatchForm()
    download_form.batch.choices = [(b.id, b.name) for b in
                                   Batch.query.order_by('_name')]
    results_form = UploadResultsForm()
    results_form.batch.choices = [(b.id, b.name) for b in
                                  Batch.query.order_by('_name')]
    if batch_form.validate_on_submit():
        tags = [Tag.query.filter_by(id=_id).first()
                for _id in batch_form.tags.data]
        batch = Batch(experiment_id=batch_form.experiment.data,
                      data_set_id=batch_form.data_set.data,
                      implementation_id=batch_form.implementation.data,
                      name=batch_form.name.data,
                      description=batch_form.description.data,
                      tags=tags,
                      params=batch_form.params.data,
                      memory=batch_form.memory.data,
                      disk=batch_form.disk.data,
                      flock=batch_form.flock.data,
                      glide=batch_form.glide.data)
        db.session.add(batch)
        db.session.commit()
        flash("New batch added successfully", "success")
        return redirect(url_for("batches.batch"))
    flash("Failed validation", "danger")
    return render_template('batches.html',
                           batch_form=batch_form,
                           download_form=download_form,
                           results_form=results_form,
                           batch_table=batch_table)


@batches.route('/download_batch', methods=["Get", "Post"])
@cache.cached(timeout=1000)
@login_required
def download_batch():
    all_batches = Batch.query.all()
    batch_items = []
    for batch in all_batches:
        b_id = batch.id
        b_name = batch.name
        b_descr = batch.description
        b_mem = batch.memory
        b_disk = batch.disk
        b_flock = batch.flock
        b_glide = batch.glide
        b_descr = batch.description
        b_tags = [tag.name for tag in Tag.query.filter(Tag.batches.any(id=b_id)).all()]
        b_exp = Experiment.query.filter(Experiment.batches.any()).first().name
        b_set = DataSet.query.filter(DataSet.batches.any()).first().name
        b_imp = Implementation.query.filter(Implementation.batches.any()).first().name
        b_size = batch.size
        b_completed = batch.completed
        batch_items.append(BatchItem(b_id, b_name, b_exp, b_set, b_imp, b_mem, b_disk, b_flock, b_glide, b_descr, '\n'.join([str(x) for x in b_tags]), b_size, b_completed))
    batch_table = BatchTable(batch_items)

    batch_form = BatchForm(memory=MEMORY, disk=DISK, flock=FLOCK, glide=GLIDE)
    batch_form.tags.choices = [(t.id, t.name) for t in
                               Tag.query.order_by('_name')]
    batch_form.experiment.choices = [(e.id, e.name) for e in
                                     Experiment.query.order_by('_name')]
    batch_form.implementation.choices = [(i.id, i.name) for i in
                                         Implementation.query.order_by('_name')]
    batch_form.data_set.choices = [(ds.id, ds.name) for ds in
                                   DataSet.query.order_by('_name')]
    download_form = DownloadBatchForm()
    download_form.batch.choices = [(b.id, b.name) for b in
                                   Batch.query.order_by('_name')]
    results_form = UploadResultsForm()
    results_form.batch.choices = [(b.id, b.name) for b in
                                  Batch.query.order_by('_name')]
    if download_form.validate_on_submit():
        batch = Batch.query.filter_by(id=download_form.batch.data).first()
        zip_file = batch.package()
        flash("Download Started", "success")
        return send_from_directory(current_app.config['STAGING_AREA'],
                                   zip_file,
                                   as_attachment=True)
    flash("Failed validation", "danger")
    return render_template('batches.html',
                           batch_form=batch_form,
                           download_form=download_form,
                           results_form=results_form,
                           batch_table=batch_table)


@batches.route('/upload_results', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def upload_results():
    
    all_batches = Batch.query.all()
    batch_items = []
    for batch in all_batches:
        b_id = batch.id
        b_name = batch.name
        b_descr = batch.description
        b_mem = batch.memory
        b_disk = batch.disk
        b_flock = batch.flock
        b_glide = batch.glide
        b_descr = batch.description
        b_tags = [tag.name for tag in Tag.query.filter(Tag.batches.any(id=b_id)).all()]
        b_exp = Experiment.query.filter(Experiment.batches.any()).first().name
        b_set = DataSet.query.filter(DataSet.batches.any()).first().name
        b_imp = Implementation.query.filter(Implementation.batches.any()).first().name
        b_size = batch.size
        b_completed = batch.completed
        batch_items.append(BatchItem(b_id, b_name, b_exp, b_set, b_imp, b_mem, b_disk, b_flock, b_glide, b_descr, '\n'.join([str(x) for x in b_tags]), b_size, b_completed))
    batch_table = BatchTable(batch_items)

    """Add the results form a batch to MongoDB job by job"""
    batch_form = BatchForm(memory=MEMORY, disk=DISK, flock=FLOCK, glide=GLIDE)
    batch_form.tags.choices = [(t.id, t.name) for t in
                               Tag.query.order_by('_name')]
    batch_form.experiment.choices = [(e.id, e.name) for e in
                                     Experiment.query.order_by('_name')]
    batch_form.implementation.choices = [(i.id, i.name) for i in
                                         Implementation.query.order_by('_name')]
    batch_form.data_set.choices = [(ds.id, ds.name) for ds in
                                   DataSet.query.order_by('_name')]
    download_form = DownloadBatchForm()
    download_form.batch.choices = [(b.id, b.name) for b in
                                   Batch.query.order_by('_name')]
    results_form = UploadResultsForm()
    results_form.batch.choices = [(b.id, b.name) for b in
                                  Batch.query.order_by('_name')]
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
                           batch_form=batch_form,
                           download_form=download_form,
                           results_form=results_form,
                           batch_table=batch_table)

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
    def __init__(self, id, name, exp, set, imp, mem, disk, flock, glide, descr, tags, size, completed):
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

