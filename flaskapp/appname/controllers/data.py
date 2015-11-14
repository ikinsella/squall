from flask import (Blueprint,
                   render_template,
                   flash,
                   request,
                   redirect,
                   url_for)
from flask.ext.login import login_required
from appname.extensions import cache
from appname.forms import (DataCollectionForm,
                           DataSetForm)
from appname.models import (db, Tag, DataCollection, data_collections_tags, DataSet, data_sets_tags)


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
        = [(data_collection.id, data_collection.name) for data_collection in DataCollection.query.order_by('name')]
    return render_template('data.html',
                           collection_form=collection_form,
                           data_set_form=data_set_form)


@data.route('/save_collection', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_collection():
    """ Save The New Data Collection """
        # store data collection name and description
    data_collection_form = DataCollectionForm()
    data_collection_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    if data_collection_form.validate_on_submit():
        new_collection = DataCollection(data_collection_form.name.data, data_collection_form.description.data)
        db.session.add(new_collection)
        db.session.commit()

        # store data collection tags
        collection_id = DataCollection.get_id(new_collection)
        selected_tags = data_collection_form.tags.data
        for tag in selected_tags:
            new_tag = Tag.query.filter_by(id=tag).first()
            new_collection.tags.append(new_tag)
            db.session.commit()

        flash("New data collection added successfully.", "success")
    return redirect(url_for("data.get_collection"))


@data.route('/save_data_set', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_data_set():
    """ Save The New Data Collection """
        # store data collection name and description
    data_set_form = DataSetForm()
    data_set_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    data_set_form.data_collection.choices\
        = [(data_collection.id, data_collection.name) for data_collection in DataCollection.query.order_by('name')]
    if data_set_form.validate_on_submit():
        new_data_set = DataSet(data_set_form.name.data, data_set_form.address.data, data_set_form.description.data, data_set_form.data_collection.data)
        db.session.add(new_data_set)
        db.session.commit()

        new_data_collection = DataCollection.query.filter_by(id=data_set_form.data_collection.data).first()
        db.session.commit()

        # store data collection tags
        #data_set_id = DataSet.get_id(new_data_set) # think we can trash
        selected_tags = data_set_form.tags.data
        for tag in selected_tags:
            new_tag = Tag.query.filter_by(id=tag).first()
            new_data_set.tags.append(new_tag)
            db.session.commit()

        flash("New data set added successfully.", "success")
    return redirect(url_for("data.get_collection"))
