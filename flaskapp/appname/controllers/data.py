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
from flask_table import Table, Col

data = Blueprint('data', __name__)


@data.route('/')
@cache.cached(timeout=1000)
@login_required
def collection():
    
    all_colls = DataCollection.query.all()
    coll_items = []
    for coll in all_colls:
        coll_id = coll.id
        coll_name = coll.name
        coll_descr = coll.description
        coll_tags = [tag.name for tag in Tag.query.filter(Tag.data_collections.any(id=coll_id)).all()]
        coll_items.append(CollItem(coll_id, coll_name, coll_descr, '\n'.join([str(x) for x in coll_tags])))
    coll_table = CollTable(coll_items)

    all_sets = DataSet.query.all()
    set_items = []
    for set in all_sets:
        set_id = set.id
        set_name = set.name
        set_descr = set.description
        set_collid = DataCollection.query.filter(DataCollection.data_sets.any(id=set.data_collection_id)).first().name
        set_urls = [url._url for url in set._urls]
        urls = '\n'.join([str(x) for x in set_urls])
        set_tags = [tag.name for tag in Tag.query.filter(Tag.data_sets.any(id=set_id)).all()]
        set_items.append(SetItem(set_id, set_name, set_descr, set_collid, urls, '\n'.join([str(x) for x in set_tags])))
    set_table = SetTable(set_items)
    
    collection_form = DataCollectionForm()
    collection_form.tags.choices = [(t.id, t.name) for t in
                                    Tag.query.order_by('_name')]
    data_set_form = DataSetForm(url_forms=URLS)
    data_set_form.tags.choices = [(t.id, t.name) for t in
                                  Tag.query.order_by('_name')]
    data_set_form.data_collection.choices = [(dc.id, dc.name) for dc in
                                             DataCollection.query.order_by(
                                                 '_name')]
    return render_template('data.html',
                           collection_form=collection_form,
                           data_set_form=data_set_form,
                           coll_table=coll_table,
                           set_table=set_table)


@data.route('/submit_collection', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_collection():
    
    all_colls = DataCollection.query.all()
    coll_items = []
    for coll in all_colls:
        coll_id = coll.id
        coll_name = coll.name
        coll_descr = coll.description
        coll_tags = [tag.name for tag in Tag.query.filter(Tag.data_collections.any(id=coll_id)).all()]
        coll_items.append(CollItem(coll_id, coll_name, coll_descr, '\n'.join([str(x) for x in coll_tags])))
    coll_table = CollTable(coll_items)

    all_sets = DataSet.query.all()
    set_items = []
    for set in all_sets:
        set_id = set.id
        set_name = set.name
        set_descr = set.description
        set_collid = DataCollection.query.filter(DataCollection.data_sets.any(id=set.data_collection_id)).first().name
        set_urls = [url._url for url in set._urls]
        urls = '\n'.join([str(x) for x in set_urls])
        set_tags = [tag.name for tag in Tag.query.filter(Tag.data_sets.any(id=set_id)).all()]
        set_items.append(SetItem(set_id, set_name, set_descr, set_collid, urls, '\n'.join([str(x) for x in set_tags])))
    set_table = SetTable(set_items)

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
                           data_set_form=data_set_form,
                           coll_table=coll_table,
                           set_table=set_table)


@data.route('/submit_data_set', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_data_set():
    
    all_colls = DataCollection.query.all()
    coll_items = []
    for coll in all_colls:
        coll_id = coll.id
        coll_name = coll.name
        coll_descr = coll.description
        coll_tags = [tag.name for tag in Tag.query.filter(Tag.data_collections.any(id=coll_id)).all()]
        coll_items.append(CollItem(coll_id, coll_name, coll_descr, '\n'.join([str(x) for x in coll_tags])))
    coll_table = CollTable(coll_items)

    all_sets = DataSet.query.all()
    set_items = []
    for set in all_sets:
        set_id = set.id
        set_name = set.name
        set_descr = set.description
        sset_collid = DataCollection.query.filter(DataCollection.data_sets.any(id=set.data_collection_id)).first().name
        set_urls = [url._url for url in set._urls]
        urls = '\n'.join([str(x) for x in set_urls])
        set_tags = [tag.name for tag in Tag.query.filter(Tag.data_sets.any(id=set_id)).all()]
        set_items.append(SetItem(set_id, set_name, set_descr, set_collid, urls, '\n'.join([str(x) for x in set_tags])))
    set_table = SetTable(set_items)
    
    collection_form = DataCollectionForm()
    collection_form.tags.choices = [(t.id, t.name) for t in
                                    Tag.query.order_by('_name')]
    data_set_form = DataSetForm(url_forms=URLS)
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
                           data_set_form=data_set_form,
                           coll_table=coll_table,
                           set_table=set_table)

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

