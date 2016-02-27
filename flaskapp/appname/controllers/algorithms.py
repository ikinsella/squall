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
from appname.controllers.constants import (URLS, SCRIPTS)


algorithms = Blueprint('algorithms', __name__)


@algorithms.route('/')
@cache.cached(timeout=1000)
@login_required
def algorithm():
    algorithm_form = AlgorithmForm()
    algorithm_form.tags.choices = [(t.id, t.name) for t in
                                   Tag.query.order_by('_name')]
    implementation_form = ImplementationForm(url_forms=URLS,
                                             setup_scripts=SCRIPTS)
    implementation_form.algorithm.choices = [(a.id, a.name) for a in
                                             Algorithm.query.order_by('_name')]
    implementation_form.tags.choices = [(t.id, t.name) for t in
                                        Tag.query.order_by('_name')]
    return render_template('algorithms.html',
                           algorithm_form=algorithm_form,
                           implementation_form=implementation_form)


@algorithms.route('/submit_algorithm', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_algorithm():
    algorithm_form = AlgorithmForm()
    algorithm_form.tags.choices = [(t.id, t.name) for t in
                                   Tag.query.order_by('_name')]
    implementation_form = ImplementationForm(url_forms=URLS,
                                             setup_scripts=SCRIPTS)
    implementation_form.algorithm.choices = [(a.id, a.name) for a in
                                             Algorithm.query.order_by('_name')]
    implementation_form.tags.choices = [(t.id, t.name) for t in
                                        Tag.query.order_by('_name')]
    if algorithm_form.validate_on_submit():
        tags = [Tag.query.filter_by(id=_id).first()
                for _id in algorithm_form.tags.data]
        algorithm = Algorithm(name=algorithm_form.name.data,
                              description=algorithm_form.description.data,
                              tags=tags)
        db.session.add(algorithm)
        db.session.commit()
        flash("New algorithm added successfully.", "success")
        return redirect(url_for("algorithms.algorithm"))
    flash('Failed validation', 'danger')
    return render_template('algorithms.html',
                           algorithm_form=algorithm_form,
                           implementation_form=implementation_form)


@algorithms.route('/submit_implementation', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_implementation():
    algorithm_form = AlgorithmForm()
    algorithm_form.tags.choices = [(t.id, t.name) for t in
                                   Tag.query.order_by('_name')]
    implementation_form = ImplementationForm(url_forms=URLS, setup_scripts=SCRIPTS)
    implementation_form.algorithm.choices = [(a.id, a.name) for a in
                                             Algorithm.query.order_by('_name')]
    implementation_form.tags.choices = [(t.id, t.name) for t in
                                        Tag.query.order_by('_name')]
    if implementation_form.validate_on_submit():
        tags = [Tag.query.filter_by(id=_id).first()
                for _id in implementation_form.tags.data]
        implementation = Implementation(
            algorithm_id=implementation_form.algorithm.data,
            name=implementation_form.name.data,
            description=implementation_form.description.data,
            tags=tags,
            urls=[url_form.url.data for url_form in
                  implementation_form.url_forms],
            setup_scripts=[script.path.data for script in
                           implementation_form.setup_scripts],
            executable=implementation_form.executable.data)
        db.session.add(implementation)
        db.session.commit()
        flash("New implementation added successfully", "success")
        return redirect(url_for("algorithms.algorithm"))
    flash('Failed validation', 'danger')
    return render_template('algorithms.html',
                           algorithm_form=algorithm_form,
                           implementation_form=implementation_form)
