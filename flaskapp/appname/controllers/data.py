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


data = Blueprint('data', __name__)


@data.route('/')
@cache.cached(timeout=1000)
@login_required
def get_collection():
    collection_form = DataCollectionForm()
    collection_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    data_set_form = DataSetForm()
    data_set_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    data_set_form.data_collection.choices\
        = [(dc.id, dc.name) for dc in DataCollection.query.order_by('name')]
    return render_template('data.html',
                           collection_form=collection_form,
                           data_set_form=data_set_form)


@data.route('/save_collection', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_collection():
    data_collection_form = DataCollectionForm()
    data_collection_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    if data_collection_form.validate_on_submit():
        tags = [Tag.query.filter_by(id=_id).first()
                for _id in data_collection_form.tags.data]
        collection = DataCollection(
            name=data_collection_form.name.data,
            description=data_collection_form.description.data,
            tags=tags)
        db.session.add(collection)
        db.session.commit()
        flash("New data collection added successfully.", "success")
    else:
        flash('Failed validation', 'danger')
    return redirect(url_for("data.get_collection"))


@data.route('/save_data_set', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_data_set():
    data_set_form = DataSetForm()
    data_set_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    data_set_form.data_collection.choices\
        = [(dc.id, dc.name) for dc in DataCollection.query.order_by('name')]
    if data_set_form.validate_on_submit():
        tags = [Tag.query.filter_by(id=_id).first()
                for _id in data_set_form.tags.data]
        data_set = DataSet(
            data_collection_id=data_set_form.data_collection.data,
            name=data_set_form.name.data,
            description=data_set_form.description.data,
            tags=tags,
            urls=data_set_form.urls.data)
        db.session.add(data_set)
        db.session.commit()
        flash("New data set added successfully.", "success")
    else:
        flash('Failed validation', 'danger')
    return redirect(url_for("data.get_collection"))
