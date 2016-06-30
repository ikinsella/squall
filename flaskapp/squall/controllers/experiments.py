from flask import (Blueprint,
                   render_template,
                   flash,
                   redirect,
                   url_for,
                   current_app,
                   send_from_directory, request, json, jsonify)
from flask.ext.login import login_required
from squall.extensions import cache
from squall.forms import (ExperimentForm,
                          ExperimentViewForm,
                          BatchForm,
                          DownloadBatchForm,
                          UploadResultsForm)
from squall.models import (db,
                           mongo,
                           Tag,
                           DataCollection,
                           Algorithm,
                           Experiment, Implementation, DataSet, Batch)
from squall.controllers.constants import (MEMORY,
                                          DISK,
                                          FLOCK,
                                          GLIDE)
from flask_table import (Table, Col)


experiments = Blueprint('experiments', __name__)


@experiments.route('/')
@cache.cached(timeout=1000)
@login_required
def experiment():
    """ """
    return render_template('experiments.html',
                           batch_form=create_batch_form(),
                           download_form=create_download_form(),
                           results_form=create_results_form(),
                           experiment_form=create_experiment_form(),
                           display_all_form=create_view_form())


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
                           batch_form=create_batch_form(),
                           download_form=create_download_form(),
                           results_form=create_results_form(),
                           experiment_form=experiment_form,
                           display_all_form=create_view_form())


@experiments.route('/submit_batch', methods=["Post"])
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
        return redirect(url_for("experiments.experiment"))
    flash("Failed validation", "danger")
    return render_template('experiments.html',
                           batch_form=batch_form,
                           download_form=create_download_form(),
                           results_form=create_results_form(),
                           experiment_form=create_experiment_form(),
                           display_all_form=create_view_form())


@experiments.route('/download_batch', methods=["Get", "Post"])
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
    return render_template('experiments.html',
                           batch_form=create_batch_form(),
                           download_form=download_form,
                           results_form=create_results_form(),
                           experiment_form=create_experiment_form(),
                           display_all_form=create_view_form())


@experiments.route('/upload_results', methods=["Get", "Post"])
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
        return redirect(url_for("experiments.experiment"))
    flash("Upload Failed: Validation Error", "danger")
    return render_template('experiments.html',
                           batch_form=create_batch_form(),
                           download_form=create_download_form(),
                           results_form=results_form,
                           experiment_form=create_experiment_form(),
                           display_all_form=create_view_form())


@experiments.route('/select_experiment', methods=['POST', 'GET'])
def select_experiment():
    data = json.loads(request.form.get('data'))
    expid = data['expid']
    tag_ret = ''
    coll_ret = ''
    alg_ret = ''
    batches = '<option value="0">Select Batch</option>'
    for entry in Batch.query.filter(Batch.experiment_id == expid).all():
        batches += '<option value="%i">%s</option>' % (entry.id, entry._name)
    name = Experiment.query.filter(Experiment.id == expid).first().name
    tags = [tag.name for tag in Tag.query.filter(
        Tag.experiments.any(id=expid)).all()]
    colls = [coll.name for coll in DataCollection.query.filter(
        DataCollection.experiments.any(id=expid)).all()]
    algs = [alg.name for alg in Algorithm.query.filter(
        Algorithm.experiments.any(id=expid)).all()]
    descr = Experiment.query.filter(Experiment.id == expid).first().description
    for tag in tags:
        tag_ret += '<p>%s</p>' % tag
    for coll in colls:
        coll_ret += '<p>%s</p>' % coll
    for alg in algs:
        alg_ret += '<p>%s</p>' % alg
    return jsonify({'name': name,
                    'descr': descr,
                    'tags': tag_ret,
                    'colls': coll_ret,
                    'algs': alg_ret,
                    'batches': batches})


@experiments.route('/select_batch', methods=['POST', 'GET'])
def select_batch():
    data = json.loads(request.form.get('data'))
    batchid = data['batchid']
    tag_ret = ''
    param_ret = ''
    batch = Batch.query.filter(Batch.id == batchid).first()
    name = batch.name
    exp = Experiment.query.filter(
        Experiment.batches.any(id=batchid)).first().name
    set = DataSet.query.filter(DataSet.batches.any(id=batchid)).first().name
    imp = Implementation.query.filter(
        Implementation.batches.any(id=batchid)).first().name
    params = batch.params
    mem = batch.memory
    disk = batch.disk
    flock = batch.flock
    glide = batch.glide
    descr = batch.description
    tags = [tag.name for tag in Tag.query.filter(
        Tag.batches.any(id=batchid)).all()]
    for tag in tags:
        tag_ret += '<p>%s</p>' % tag
    for param in params:
        param_ret += '<p>%s</p>' % str(param)
    return jsonify({'name': name,
                    'exp': exp,
                    'set': set,
                    'imp': imp,
                    'param': param_ret,
                    'mem': mem,
                    'disk': disk,
                    'flock': flock,
                    'glide': glide,
                    'descr': descr,
                    'tags': tag_ret})


@experiments.route('/select_upload', methods=['POST', 'GET'])
def select_upload():
    data = json.loads(request.form.get('data'))
    batchid = data['batchid']
    batch = Batch.query.filter(Batch.id == batchid).first()
    status = batch.completed
    return jsonify({'status': status})


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


def create_view_form():
    display_all_form = ExperimentViewForm()
    display_all_form.experiments.choices = [(0, 'Select Experiment')] + \
                                           [(exp.id, exp.name) for exp in
                                            Experiment.query.order_by('_name')]
    display_all_form.batches.choices = [(0, 'Select Batch')]
    return display_all_form
