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
from appname.models import (db, Tag)


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
    return render_template('data.html',
                           collection_form=collection_form,
                           data_set_form=data_set_form)


@data.route('/save_collection', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_collection():
    """ Save The New Data Collection """
    flash("The Data Collection Will Have Been Saved", "success")
    return redirect(url_for("data.get_collection"))


@data.route('/save_data_set', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_data_set():
    """ Save The New Data Collection """
    flash("The Data Set Will Have Been Saved", "success")
    return redirect(url_for("data.get_collection"))
