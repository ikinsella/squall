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
                            mongodb,
                            Tag,
                            Experiment,
                            Implementation,
                            DataSet,
                            Batch)
from appname.controllers.constants import (MEMORY,
                                           DISK,
                                           FLOCK,
                                           GLIDE)

batches = Blueprint('batches', __name__)


@batches.route('/')
@cache.cached(timeout=1000)
@login_required
def batch():
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
                           results_form=results_form)


@batches.route('/submit_batch', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_batch():
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
                           results_form=results_form)


@batches.route('/download_batch', methods=["Get", "Post"])
@cache.cached(timeout=1000)
@login_required
def download_batch():
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
                           results_form=results_form)


@batches.route('/upload_results', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def upload_results():
    #mongotest
    #post = {"author":"My name is Zach"}  
    #posts = mongodb.posts  
    #result = posts.insert(post)              
    #flash(dict(post))
    #for post in posts.find():                
    #    print post
    #return redirect(url_for("algorithms.algorithm"))




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
        results_json = json.load(results_form.results.data) # TODO: Handle Results File Uploads
        batch = Batch.query.filter_by(id=results_form.batch.data).first()
        batch.results = results_json  # TODO: Link results to batch 
	exp = Experiment.query.filter_by(id=batch.experiment_id).first()
	if exp.name in mongodb.collection_names():
		col = mongodb.create_collection(exp.name)
	else:
		col = mongodb[exp.name]
	b_post = batch.getMongoInfo
	for key, value in results_json.iteritems():
		post = {'id': key}
		post.update(b_post)
		post.update({'results':value})
		result = col.insert(post)
        flash("Results Stored", "danger")
        return redirect(url_for("batches.batch"))
    flash("Failed validation", "danger")

    return render_template('batches.html',
                           batch_form=batch_form,
                           download_form=download_form,
                           results_form=results_form)
