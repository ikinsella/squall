from flask import (Blueprint,
                   render_template,
                   flash,
                   redirect,
                   url_for, request, json, jsonify)
from flask.ext.login import login_required
from squall.extensions import cache
from squall.forms import (AlgorithmForm,
                          ImplementationForm,
                          AlgorithmViewForm)
from squall.models import (db,
                           Tag,
                           Algorithm,
                           Implementation, URL)
from squall.controllers.constants import (URLS, SCRIPTS)
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
                           imp_table=create_implementation_table(),
                           display_all_form=create_view_form())


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
                           imp_table=create_implementation_table(),
                           display_all_form=create_view_form())


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
                           imp_table=create_implementation_table(),
                           display_all_form=create_view_form())

@algorithms.route('/narrow', methods=['POST', 'GET'])
def narrow():
    data = json.loads(request.form.get('data'))
    algid = data['algid']
    imps = '<option value="0">Select Implementation</option>'
    tag_ret = ''
    for entry in Implementation.query.filter(Implementation._algorithm_id == algid).all():
        imps += '<option value="%i">%s</option>' % (entry.id, entry._name)
    name = Algorithm.query.filter(Algorithm.id==algid).first().name
    descr = Algorithm.query.filter(Algorithm.id==algid).first().description
    tags = [tag.name for tag in Tag.query.filter(Tag.algorithms.any(id=algid)).all()]
    for tag in tags:
        tag_ret += '<p>%s</p>' % tag
    return jsonify({'imps':imps, 'name':name, 'descr':descr, 'tags':tag_ret})

@algorithms.route('/select_imp', methods=['POST', 'GET'])
def select_imp():
    data = json.loads(request.form.get('data'))
    impid = data['impid']
    url_ret = ''
    script_ret = ''
    tag_ret = ''
    name = Implementation.query.filter(Implementation.id==impid).first().name
    alg = Algorithm.query.filter(Algorithm.implementations.any(id=impid)).first().name
    exe = Implementation.query.filter(Implementation.id==impid).first().executable
    descr = Implementation.query.filter(Implementation.id==impid).first().description
    tags = [tag.name for tag in Tag.query.filter(Tag.implementations.any(id=impid)).all()]
    urls = [url.url for url in URL.query.filter(URL.implementation.has(id=impid)).all()]
    scripts = Implementation.query.filter(Implementation.id==impid).first().setup_scripts
    for scr in scripts:
        script_ret += '<p>%s</p>' % scr
    for tag in tags:
        tag_ret += '<p>%s</p>' % tag
    for url in urls:
        url_ret += '<p>%s</p>' % url
    return jsonify({'name':name, 'alg':alg, 'urls':url_ret, 'scripts':script_ret, 'exe':exe, 'descr':descr, 'tags':tag_ret})


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

def create_view_form():
    display_all_form = AlgorithmViewForm()
    display_all_form.algorithms.choices = [(0, 'Select Algorithm')]+[(da.id, da.name) for da in
                                                                     Algorithm.query.order_by('_name')]
    display_all_form.implementations.choices = [(0, 'Select Implementation')]
    return display_all_form


