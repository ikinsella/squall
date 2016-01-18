from flask import (Blueprint,
                   render_template,
                   flash,
                   redirect,
                   url_for)
from flask.ext.login import login_required
from appname.extensions import cache
from appname.forms import (AlgorithmForm,
                           ImplementationForm)
from appname.models import (db,
                            Tag,
                            Algorithm,
                            Implementation)


algorithms = Blueprint('algorithms', __name__)


@algorithms.route('/')
@cache.cached(timeout=1000)
@login_required
def get_algorithm():
    # Algorithm Form
    algorithm_form = AlgorithmForm()
    algorithm_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('_name')]
    # Implementation Form
    implementation_form = ImplementationForm()
    implementation_form.algorithm.choices\
        = [(algorithm.id, algorithm.name)
           for algorithm in Algorithm.query.order_by('_name')]
    implementation_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('_name')]
    return render_template('algorithms.html',
                           algorithm_form=algorithm_form,
                           implementation_form=implementation_form)


@algorithms.route('/save_algorithm', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_algorithm():
    algorithm_form = AlgorithmForm()
    algorithm_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('_name')]
    if algorithm_form.validate_on_submit():
        tags = [Tag.query.filter_by(id=_id).first()
                for _id in algorithm_form.tags.data]
        algorithm = Algorithm(name=algorithm_form.name.data,
                              description=algorithm_form.description.data,
                              tags=tags)
        db.session.add(algorithm)
        db.session.commit()
        flash("New algorithm added successfully.", "success")
    else:
        flash('Failed validation', 'danger')
    return redirect(url_for("algorithms.get_algorithm"))


@algorithms.route('/save_implementation', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def save_implementation():
    implementation_form = ImplementationForm()
    implementation_form.tags.choices\
        = [(tag.id, tag.name) for tag in Tag.query.order_by('_name')]
    implementation_form.algorithm.choices\
        = [(algorithm.id, algorithm.name)
           for algorithm in Algorithm.query.order_by('_name')]
    if implementation_form.validate_on_submit():
        tags = [Tag.query.filter_by(id=_id).first()
                for _id in implementation_form.tags.data]
        implementation = Implementation(
            algorithm_id=implementation_form.algorithm.data,
            name=implementation_form.name.data,
            description=implementation_form.description.data,
            tags=tags,
            urls=implementation_form.urls.data,
            setup_scripts=implementation_form.setup_scripts.data,
            executable=implementation_form.executable.data)
        db.session.add(implementation)
        db.session.commit()
        flash("New implementation added successfully", "success")
    else:
        flash('Failed validation', 'danger')
    return redirect(url_for("algorithms.get_algorithm"))
