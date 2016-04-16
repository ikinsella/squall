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
from flask_table import (Table, Col)


algorithms = Blueprint('algorithms', __name__)


@algorithms.route('/')
@cache.cached(timeout=1000)
@login_required
def algorithm():
    """ """
    return render_template('algorithms.html',
                           algorithm_form=create_algorithm_form(),
                           implementation_form=create_implementation_form(),
                           alg_table=create_algorithm_table(),
                           imp_table=create_implementation_table())


@algorithms.route('/submit_algorithm', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_algorithm():
    """ """
    algorithm_form = create_algorithm_form()
    if algorithm_form.validate_on_submit():
        db.session.add(Algorithm(name=algorithm_form.name.data,
                                 description=algorithm_form.description.data,
                                 tags=[Tag.query.filter_by(id=_id).first()
                                       for _id in algorithm_form.tags.data]))
        db.session.commit()
        flash("New algorithm added successfully.", "success")
        return redirect(url_for("algorithms.algorithm"))
    flash('Failed validation', 'danger')
    return render_template('algorithms.html',
                           algorithm_form=algorithm_form,
                           implementation_form=create_implementation_form(),
                           alg_table=create_algorithm_table(),
                           imp_table=create_implementation_table())


@algorithms.route('/submit_implementation', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_implementation():
    """ """
    implementation_form = create_implementation_form()
    if implementation_form.validate_on_submit():
        db.session.add(Implementation(
            algorithm_id=implementation_form.algorithm.data,
            name=implementation_form.name.data,
            description=implementation_form.description.data,
            tags=[Tag.query.filter_by(id=_id).first()
                  for _id in implementation_form.tags.data],
            urls=[url_form.url.data for url_form in
                  implementation_form.url_forms],
            setup_scripts=[script.path.data for script in
                           implementation_form.setup_scripts],
            executable=implementation_form.executable.data))
        db.session.commit()
        flash("New implementation added successfully", "success")
        return redirect(url_for("algorithms.algorithm"))
    flash('Failed validation', 'danger')
    return render_template('algorithms.html',
                           algorithm_form=create_algorithm_form(),
                           implementation_form=implementation_form,
                           alg_table=create_algorithm_table(),
                           imp_table=create_implementation_table())


class AlgTable(Table):
    id = Col('Algorithm ID')
    name = Col('Algorithm Name')
    description = Col('Description')
    tags = Col('Tags')

    def tr_format(self, item):
        return '<tr valign="top">{}</tr>'


class ImpTable(Table):
    id = Col('Implementation ID')
    name = Col('Implementation Name')
    description = Col('Description')
    executable = Col('Executable')
    alg = Col('Associated Algorithm')
    urls = Col('URL')
    tags = Col('Tags')

    def tr_format(self, item):
        return '<tr valign="top">{}</tr>'


class AlgItem(object):
    def __init__(self, id, name, description, tags):
        self.name = name
        self.id = id
        self.description = description
        self.tags = tags


class ImpItem(object):
    def __init__(self, id, name, description, executable, alg, urls, tags):
        self.name = name
        self.id = id
        self.description = description
        self.executable = executable
        self.alg = alg
        self.urls = urls
        self.tags = tags


def create_algorithm_table():
    """ """
    return AlgTable([AlgItem(
        alg.id,
        alg.name,
        alg.description,
        '\n'.join([str(tag.name) for tag in Tag.query.filter(
            Tag.algorithms.any(id=alg.id)).all()]))
        for alg in Algorithm.query.all()])


def create_implementation_table():
    """ """
    return ImpTable([ImpItem(
        imp.id,
        imp.name,
        imp.description,
        imp.executable,
        Algorithm.query.filter(Algorithm.implementations.any(
            id=imp._algorithm_id)).first().name,
        '\n'.join([str(url._url) for url in imp._urls]),
        '\n'.join([tag.name for tag in Tag.query.filter(
            Tag.implementations.any(id=imp.id)).all()]))
        for imp in Implementation.query.all()])


def create_algorithm_form():
    """ """
    form = AlgorithmForm()
    form.tags.choices = [(t.id, t.name) for t in Tag.query.order_by('_name')]
    return form


def create_implementation_form():
    """ """
    form = ImplementationForm(url_forms=URLS, setup_scripts=SCRIPTS)
    form.algorithm.choices = [(a.id, a.name) for a in
                              Algorithm.query.order_by('_name')]
    form.tags.choices = [(t.id, t.name) for t in Tag.query.order_by('_name')]
    return form
