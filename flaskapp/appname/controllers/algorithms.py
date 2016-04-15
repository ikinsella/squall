from flask import (Blueprint,
                   render_template,
                   flash,
                   redirect,
                   url_for)
from flask.ext.login import login_required
from appname.extensions import cache
from appname.forms import (AlgorithmForm,
                           ImplementationForm,
                           DisplayAllForm)
from appname.models import (db,
                            Tag,
                            Algorithm,
                            Implementation,
                            URL)
from appname.controllers.constants import (URLS, SCRIPTS)
from flask_table import Table, Col


algorithms = Blueprint('algorithms', __name__)


@algorithms.route('/')
@cache.cached(timeout=1000)
@login_required
def algorithm():
    
    all_algs = Algorithm.query.all()
    alg_items = []
    for alg in all_algs:
        alg_id = alg.id
        alg_name = alg.name
        alg_descr = alg.description
        alg_tags = [tag.name for tag in Tag.query.filter(Tag.algorithms.any(id=alg_id)).all()]
        alg_items.append(AlgItem(alg_id, alg_name, alg_descr, '\n'.join([str(x) for x in alg_tags])))
    alg_table = AlgTable(alg_items)

    all_imps = Implementation.query.all()
    imp_items = []
    for imp in all_imps:
        imp_id = imp.id
        imp_name = imp.name
        imp_descr = imp.description
        imp_executable = imp.executable
        imp_algid = Algorithm.query.filter(Algorithm.implementations.any(id=imp._algorithm_id)).first().name
        imp_urls = [url._url for url in imp._urls]
        urls = '\n'.join([str(x) for x in imp_urls])
        imp_tags = [tag.name for tag in Tag.query.filter(Tag.implementations.any(id=imp_id)).all()]
        imp_items.append(ImpItem(imp_id, imp_name, imp_descr, imp_executable, imp_algid, urls, '\n'.join([str(x) for x in imp_tags])))
    imp_table = ImpTable(imp_items)
                                                                            
    algorithm_form = AlgorithmForm()
    algorithm_form.tags.choices = [(t.id, t.name) for t in
                                   Tag.query.order_by('_name')]
    
    implementation_form = ImplementationForm(url_forms=URLS,
                                             setup_scripts=SCRIPTS)
    implementation_form.algorithm.choices = [(a.id, a.name) for a in
                                             Algorithm.query.order_by('_name')]
    implementation_form.tags.choices = [(t.id, t.name) for t in
                                        Tag.query.order_by('_name')]
    
#    display_all_form = DisplayAllForm()
#    display_all_form.algorithms.choices = [(da.id, da.name) for da in
#                                           Algorithm.query.order_by('_name')]
#    display_all_form.implementations.choices = ''
    return render_template('algorithms.html',
                           algorithm_form=algorithm_form,
                           implementation_form=implementation_form,
                           #display_all_form=display_all_form,
                           alg_table=alg_table,
                           imp_table=imp_table)


@algorithms.route('/submit_algorithm', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_algorithm():
    all_algs = Algorithm.query.all()
    alg_items = []
    for alg in all_algs:
        alg_id = alg.id
        alg_name = alg.name
        alg_descr = alg.description
        alg_tags = [tag.name for tag in Tag.query.filter(Tag.algorithms.any(id=alg_id)).all()]
        alg_items.append(AlgItem(alg_id, alg_name, alg_descr, '\n'.join([str(x) for x in alg_tags])))
    alg_table = AlgTable(alg_items)
    
    all_imps = Implementation.query.all()
    imp_items = []
    for imp in all_imps:
        imp_id = imp.id
        imp_name = imp.name
        imp_descr = imp.description
        imp_executable = imp.executable
        imp_algid = Algorithm.query.filter(Algorithm.implementations.any(id=imp._algorithm_id)).first().name
        imp_urls = [url._url for url in imp._urls]
        urls = '\n'.join([str(x) for x in imp_urls])
        imp_tags = [tag.name for tag in Tag.query.filter(Tag.implementations.any(id=imp_id)).all()]
        imp_items.append(ImpItem(imp_id, imp_name, imp_descr, imp_executable, imp_algid, urls, '\n'.join([str(x) for x in imp_tags])))
    imp_table = ImpTable(imp_items)
    
    algorithm_form = AlgorithmForm()
    algorithm_form.tags.choices = [(t.id, t.name) for t in
                                   Tag.query.order_by('_name')]
    
    implementation_form = ImplementationForm(url_forms=URLS,
                                             setup_scripts=SCRIPTS)
    implementation_form.algorithm.choices = [(a.id, a.name) for a in
                                             Algorithm.query.order_by('_name')]
    implementation_form.tags.choices = [(t.id, t.name) for t in
                                        Tag.query.order_by('_name')]
    
#    display_all_form = DisplayAllForm()
#    display_all_form.algorithms.choices = [(da.id, da.name) for da in
#                                           Algorithm.query.order_by('_name')]
#    display_all_form.implementations.choices = ''

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
                           implementation_form=implementation_form,
                           #display_all_form=display_all_form,
                           alg_table=alg_table,
                           imp_table=imp_table)


@algorithms.route('/submit_implementation', methods=["Post"])
@cache.cached(timeout=1000)
@login_required
def submit_implementation():
    all_algs = Algorithm.query.all()
    alg_items = []
    for alg in all_algs:
        alg_id = alg.id
        alg_name = alg.name
        alg_descr = alg.description
        alg_tags = [tag.name for tag in Tag.query.filter(Tag.algorithms.any(id=alg_id)).all()]
        alg_items.append(AlgItem(alg_id, alg_name, alg_descr, '\n'.join([str(x) for x in alg_tags])))
    alg_table = AlgTable(alg_items)
    
    all_imps = Implementation.query.all()
    imp_items = []
    for imp in all_imps:
        imp_id = imp.id
        imp_name = imp.name
        imp_descr = imp.description
        imp_executable = imp.executable
        imp_algid = Algorithm.query.filter(Algorithm.implementations.any(id=imp._algorithm_id)).first().name
        imp_urls = [url._url for url in imp._urls]
        urls = '\n'.join([str(x) for x in imp_urls])
        imp_tags = [tag.name for tag in Tag.query.filter(Tag.implementations.any(id=imp_id)).all()]
        imp_items.append(ImpItem(imp_id, imp_name, imp_descr, imp_executable, imp_algid, urls, '\n'.join([str(x) for x in imp_tags])))
    imp_table = ImpTable(imp_items)
                                                                            
    algorithm_form = AlgorithmForm()
    algorithm_form.tags.choices = [(t.id, t.name) for t in
                                   Tag.query.order_by('_name')]
    
    implementation_form = ImplementationForm(url_forms=URLS, setup_scripts=SCRIPTS)
    implementation_form.algorithm.choices = [(a.id, a.name) for a in
                                             Algorithm.query.order_by('_name')]
    implementation_form.tags.choices = [(t.id, t.name) for t in
                                        Tag.query.order_by('_name')]
    
#    display_all_form = DisplayAllForm()
#    display_all_form.algorithms.choices = [(da.id, da.name) for da in
#                                           Algorithm.query.order_by('_name')]
#    display_all_form.implementations.choices = ''

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
                           implementation_form=implementation_form,
                           #display_all_form=display_all_form,
                           alg_table=alg_table,
                           imp_table=imp_table)

#@algorithms.route('/narrow', methods=['POST', 'GET'])
#def narrow():
#    display_all_form = DisplayAllForm()
#    display_all_form.algorithms.choices = [(da.id, da.name) for da in
#                                           Algorithm.query.order_by('_name')]
#    display_all_form.implementations.choices = ''
#    ret = ''
#    for entry in Implementation.query.filter(Implementation._algorithm_id == display_all_form.algorithms.data).order_by('_name'):
#        ret += '<option value="%i">%s</option>' % (entry.key, entry.value)
#    return ret

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






