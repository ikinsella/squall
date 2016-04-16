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
from flask_table import (Table, Col)

data = Blueprint('data', __name__)


@data.route('/')
@cache.cached(timeout=1000)
@login_required
def collection():
    return render_template('data.html',
                           collection_form=create_collection_form(),
                           data_set_form=create_data_set_form(),
                           coll_table=create_collection_table(),
                           set_table=create_data_set_table())


@data.route('/submit_collection', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_collection():
    """ """
    collection_form = create_collection_form()
    if collection_form.validate_on_submit():
        db.session.add(DataCollection(
            name=collection_form.name.data,
            description=collection_form.description.data,
            tags=[Tag.query.filter_by(id=_id).first()
                  for _id in collection_form.tags.data]))
        db.session.commit()
        flash("New data collection added successfully.", "success")
        return redirect(url_for("data.collection"))
    flash('Failed validation', 'danger')
    return render_template('data.html',
                           collection_form=collection_form,
                           data_set_form=create_data_set_form(),
                           coll_table=create_collection_table(),
                           set_table=create_data_set_table())


@data.route('/submit_data_set', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_data_set():
    """ """
    data_set_form = create_data_set_form()
    if data_set_form.validate_on_submit():
        db.session.add(DataSet(
            data_collection_id=data_set_form.data_collection.data,
            name=data_set_form.name.data,
            description=data_set_form.description.data,
            tags=[Tag.query.filter_by(id=_id).first()
                  for _id in data_set_form.tags.data],
            urls=[url_form.url.data for url_form in data_set_form.url_forms]))
        db.session.commit()
        flash("New data set added successfully.", "success")
        return redirect(url_for("data.collection"))
    flash('Failed validation', 'danger')
    return render_template('data.html',
                           collection_form=create_collection_form(),
                           data_set_form=data_set_form,
                           coll_table=create_collection_table(),
                           set_table=create_data_set_table())


class CollTable(Table):
    id = Col('Data Collection ID')
    name = Col('Data Collection Name')
    description = Col('Description')
    tags = Col('Tags')

    def tr_format(self, item):
        return '<tr valign="top">{}</tr>'


class SetTable(Table):
    id = Col('Data Set ID')
    name = Col('Data Set Name')
    description = Col('Description')
    data_collection = Col('Assoc Data Collection')
    urls = Col('URLs')
    tags = Col('Tags')

    def tr_format(self, item):
        return '<tr valign="top">{}</tr>'


class CollItem(object):
    def __init__(self, id, name, description, tags):
        self.name = name
        self.id = id
        self.description = description
        self.tags = tags


class SetItem(object):
    def __init__(self, id, name, description, data_collection, urls, tags):
        self.name = name
        self.id = id
        self.description = description
        self.data_collection = data_collection
        self.urls = urls
        self.tags = tags


def create_collection_table():
    """ """
    return CollTable([CollItem(
        coll.id,
        coll.name,
        coll.description,
        '\n'.join([str(tag.name) for tag in Tag.query.filter(
            Tag.data_collections.any(
                id=coll.id)).all()])) for coll in DataCollection.query.all()])


def create_data_set_table():
    """ """
    return SetTable([SetItem(
        set.id,
        set.name,
        set.description,
        DataCollection.query.filter(
            DataCollection.data_sets.any(
                id=set.data_collection_id)).first().name,
        '\n'.join([str(url._url) for url in set._urls]),
        '\n'.join([str(tag.name) for tag in Tag.query.filter(Tag.data_sets.any(
            id=set.id)).all()])) for set in DataSet.query.all()])


def create_collection_form():
    form = DataCollectionForm()
    form.tags.choices = [(t.id, t.name) for t in
                         Tag.query.order_by('_name')]
    return form


def create_data_set_form():
    form = DataSetForm(url_forms=URLS)
    form.tags.choices = [(t.id, t.name) for t in
                         Tag.query.order_by('_name')]
    form.data_collection.choices = [(dc.id, dc.name) for dc in
                                    DataCollection.query.order_by('_name')]
    return form
