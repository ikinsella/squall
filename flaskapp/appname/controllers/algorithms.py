from flask import (Blueprint,
                   render_template,
                   flash,
                   request,
                   redirect,
                   url_for)
from flask.ext.login import login_required
from appname.extensions import cache
from appname.forms import (AlgorithmForm,
                           ImplementationForm)
from appname.models import (db, Tag, Algorithm, algorithms_tags)


algorithms = Blueprint('algorithms', __name__)


@algorithms.route('/')
@cache.cached(timeout=1000)
@login_required
def get_algorithm():
    algorithm_form = AlgorithmForm()
    algorithm_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    implementation_form = ImplementationForm()
    implementation_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    return render_template('algorithms.html',
                           algorithm_form=algorithm_form,
                           implementation_form=implementation_form)


@algorithms.route('/save_algorithm', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_algorithm():
    """Save The New Algorithm"""
    # store algorithm name and description
    algorithm_form = AlgorithmForm()
    algorithm_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
    if algorithm_form.validate_on_submit():
        new_alg = Algorithm(algorithm_form.name.data, algorithm_form.description.data)
        db.session.add(new_alg)
        db.session.commit()

        # store algorithm tags
        alg_id = Algorithm.get_id(new_alg)
        selected_tags = algorithm_form.tags.data
        for tag in selected_tags:
            new_tag = Tag.query.filter_by(id=tag).first()
            new_alg.tags.append(new_tag)
            db.session.commit()

        flash("New algorithm added successfully.", "success")

    return redirect(url_for("algorithms.get_algorithm"))


@algorithms.route('/save_implementation', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_implementation():
    flash("The Implementation Will Have Been Saved")
    return redirect(url_for("algs.get_algorithm"))
