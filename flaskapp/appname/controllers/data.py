from flask import (Blueprint,
                   render_template,
                   flash,
                   redirect,
                   url_for)
from flask.ext.login import login_required
from appname.extensions import cache
from appname.forms import (DataCollectionForm,
                           DataSetForm)
from appname.models import (db,
                            Tag,
                            DataCollection,
                            DataSet)
from appname.controllers.constants import URLS

data = Blueprint('data', __name__)


@data.route('/')
@cache.cached(timeout=1000)
@login_required
def collection():
    collection_form = DataCollectionForm()
    collection_form.tags.choices = [(t.id, t.name) for t in
                                    Tag.query.order_by('_name')]
    data_set_form = DataSetForm(urls=URLS)
    data_set_form.tags.choices = [(t.id, t.name) for t in
                                  Tag.query.order_by('_name')]
    data_set_form.data_collection.choices = [(dc.id, dc.name) for dc in
                                             DataCollection.query.order_by(
                                                 '_name')]
    return render_template('data.html',
                           collection_form=collection_form,
                           data_set_form=data_set_form)


@data.route('/submit_collection', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_collection():
    collection_form = DataCollectionForm()
    collection_form.tags.choices = [(t.id, t.name) for t in
                                    Tag.query.order_by('_name')]
    data_set_form = DataSetForm(url_forms=URLS)
    data_set_form.tags.choices = [(t.id, t.name) for t in
                                  Tag.query.order_by('_name')]
    data_set_form.data_collection.choices = [(dc.id, dc.name) for dc in
                                             DataCollection.query.order_by(
                                                 '_name')]
    if collection_form.validate_on_submit():
        tags = [Tag.query.filter_by(id=_id).first()
                for _id in collection_form.tags.data]
        collection = DataCollection(
            name=collection_form.name.data,
            description=collection_form.description.data,
            tags=tags)
        db.session.add(collection)
        db.session.commit()
        flash("New data collection added successfully.", "success")
        return redirect(url_for("data.collection"))
    flash('Failed validation', 'danger')
    return render_template('data.html',
                           collection_form=collection_form,
                           data_set_form=data_set_form)


@data.route('/submit_data_set', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_data_set():
    collection_form = DataCollectionForm()
    collection_form.tags.choices = [(t.id, t.name) for t in
                                    Tag.query.order_by('_name')]
    data_set_form = DataSetForm(urls=URLS)
    data_set_form.tags.choices = [(t.id, t.name) for t in
                                  Tag.query.order_by('_name')]
    data_set_form.data_collection.choices = [(dc.id, dc.name) for dc in
                                             DataCollection.query.order_by(
                                                 '_name')]
    if data_set_form.validate_on_submit():
        tags = [Tag.query.filter_by(id=_id).first()
                for _id in data_set_form.tags.data]
        data_set = DataSet(
            data_collection_id=data_set_form.data_collection.data,
            name=data_set_form.name.data,
            description=data_set_form.description.data,
            tags=tags,
            urls=[url_form.url.data for url_form in data_set_form.url_forms])
        db.session.add(data_set)
        db.session.commit()
        flash("New data set added successfully.", "success")
        return redirect(url_for("data.collection"))
    flash('Failed validation', 'danger')
    return render_template('data.html',
                           collection_form=collection_form,
                           data_set_form=data_set_form)
