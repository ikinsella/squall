import os
import shutil
import json
import yaml
import zipfile
import re

from flask import (render_template, current_app)
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import (UserMixin, AnonymousUserMixin)
from werkzeug.security import (generate_password_hash, check_password_hash)
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.pymongo import PyMongo

db = SQLAlchemy()
mongo = PyMongo()

""" Tables For Many To Many Relationships """
""" TODO : Multi-User
users_tags = db.Table(
    'users_tags',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))
"""
algorithms_experiments = db.Table(
    'algorithms_experiments',
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id')),
    db.Column('algorithm_id', db.Integer, db.ForeignKey('algorithm.id')))

algorithms_tags = db.Table(
    'algorithms_tags',
    db.Column('algorithm_id', db.Integer, db.ForeignKey('algorithm.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

implementations_tags = db.Table(
    'implementations_tags',
    db.Column('implementation_id', db.Integer,
              db.ForeignKey('implementation.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

collections_experiments = db.Table(
    'collections_experiments',
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id')),
    db.Column('collection_id', db.Integer,
              db.ForeignKey('data_collection.id')))

collections_tags = db.Table(
    'collections_tags',
    db.Column('data_collection_id', db.Integer,
              db.ForeignKey('data_collection.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

data_sets_tags = db.Table(
    'data_sets_tags',
    db.Column('data_set_id', db.Integer, db.ForeignKey('data_set.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

experiments_tags = db.Table(
    'experiments_tags',
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

batches_tags = db.Table(
    'batches_tags',
    db.Column('batch_id', db.Integer, db.ForeignKey('batch.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

""" Entities """


class User(db.Model, UserMixin):
    """Represents a single User who has access to the application"""

    # Fields
    id = db.Column(db.Integer(), primary_key=True)
    _launch_directory = db.Column(db.String(128))
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    """ TODO: Multi-User
    _tags = db.relationship('Tag', secondary=users_tags,
                            backref=db.backref('users',
                                               lazy='dynamic'))
    """
    # relationships
    """ TODO: Multi-User
    algorithms = db.relationship()
    datacollections = db.relationship()
    experiments = db.relationship()
    batches = db.relationship()
    tags = db.relationship()
    """

    def __init__(self, username, launch_directory, password):
        self.username = username
        self._launch_directory = launch_directory
        self.set_password(password)

    def __repr__(self):
        return '<User {username}>'.format(username=self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def get_id(self):
        return unicode(self.id)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    @hybrid_property
    def launch_directory(self):
        return self._launch_directory

    @launch_directory.setter
    def launch_directory(self, value):
        self._launch_directory = value


class Tag(db.Model):
    """Represents a tag which is used to add query-able meta data
     to experiments, batches, data collections, data sets, algorithms,
     and implementations. A User defines tags in a view and each collected
     job is associated with all the tags contained in its hierarchy."""

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(64), index=True, unique=True)

    # Relationships
    """ TODO: Multi-User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """

    def __init__(self, name):
        super(Tag, self).__init__()
        self._name = name

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class Algorithm(db.Model):
    """ Entity representing a single algorithm used in a an experiment """

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(64), index=True, unique=True)
    _description = db.Column(db.String(512), index=False, unique=False)

    # Relationships
    """ TODO: Multi-User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """
    _tags = db.relationship('Tag', secondary=algorithms_tags,
                            backref=db.backref('algorithms', lazy='dynamic'))
    _implementations = db.relationship('Implementation', backref='algorithm',
                                       lazy='dynamic')

    def __init__(self, name, description, tags):
        self._name = name
        self._description = description
        self._tags = tags

    @hybrid_property
    def serialize(self):
        return {'Name': self.name,
                'Tags': [tag.name for tag in self.tags]}

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @hybrid_property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @hybrid_property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags.append(value)

    @hybrid_property
    def implementations(self):
        return self._implementations

    @implementations.setter
    def implementations(self, value):
        self._implementations.append(value)


class Implementation(db.Model):
    """Represents a single implementation of an algorithm"""

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(64), index=True, unique=True)
    _description = db.Column(db.String(512), index=False, unique=False)
    _setup_scripts = db.Column(db.PickleType(), index=False, unique=False)
    _executable = db.Column(db.String(64), index=False, unique=False)

    # Relationships
    _algorithm_id = db.Column(db.Integer, db.ForeignKey('algorithm.id'))
    """ TODO: Multi-User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """
    _tags = db.relationship('Tag', secondary=implementations_tags,
                            backref=db.backref('implementations',
                                               lazy='dynamic'))
    _urls = db.relationship('URL', backref='implementation', lazy='select')
    _batches = db.relationship('Batch', backref='implementation',
                               lazy='dynamic')
    """ TODO: Parameter Validation
    _arguments = db.relationship('Argument',
                                 backref='implementation',
                                 lazy='dynamic')
    """

    def __init__(self,
                 algorithm_id,
                 name,
                 description,
                 tags,
                 urls,
                 setup_scripts,
                 executable):
        self._algorithm_id = algorithm_id
        self._name = name
        self._description = description
        self._tags = tags
        self._urls = [URL(url, implementation_id=self.id) for url in urls]
        self._setup_scripts = setup_scripts
        self._executable = executable
        # self._arguments = arguments  # TODO: Parameter Validation

    @hybrid_property
    def serialize(self):
        return {'Name': self.name,
                'Tags': [tag.name for tag in self.tags]}

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @hybrid_property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @hybrid_property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags.append(value)

    @hybrid_property
    def urls(self):
        return [url.url for url in self._urls]

    @urls.setter
    def urls(self, value):
        self._urls.append(URL(value, implementation_id=self.id))

    @hybrid_property
    def setup_scripts(self):
        return self._setup_scripts

    @setup_scripts.setter
    def setup_scripts(self, value):
        self._setup_scripts.append(value)

    @hybrid_property
    def executable(self):
        return self._executable

    @executable.setter
    def executable(self, value):
        self._executable = value

    @hybrid_property
    def batches(self):
        return self._batches

    @batches.setter
    def batches(self, value):
        self._batches.append(value)
    """ TODO: Parameter Validation
    @hybrid_property
    def arguments(self):
        return self._arguments

    @arguments.setter
    def arguments(self, value):
        self._arguments.append(value)
    """


class DataCollection(db.Model):
    """Represents a collection of datasets derived from a common source"""

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(64), index=True, unique=True)
    _description = db.Column(db.String(512), index=False, unique=False)

    # Relationships
    """ TODO: Moving To Multi-User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """
    _tags = db.relationship('Tag', secondary=collections_tags,
                            backref=db.backref('data_collections',
                                               lazy='dynamic'))
    _data_sets = db.relationship('DataSet', backref='data_collection',
                                 lazy='dynamic')

    def __init__(self, name, description, tags):
        super(DataCollection, self).__init__()
        self._name = name
        self._description = description
        self._tags = tags

    @hybrid_property
    def serialize(self):
        return {'Name': self.name,
                'Tags': [tag.name for tag in self.tags]}

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @hybrid_property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @hybrid_property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags.append(value)

    @hybrid_property
    def data_sets(self):
        return self._data_sets

    @data_sets.setter
    def data_sets(self, value):
        self._data_sets.append(value)


class DataSet(db.Model):
    """Represents a single dataset belonging to a data collection"""

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(64), index=True, unique=True)
    _description = db.Column(db.String(512), index=False, unique=False)

    # Relationships
    """ TODO: Moving To Multi-User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """
    data_collection_id = db.Column(
        db.Integer, db.ForeignKey('data_collection.id'))
    _tags = db.relationship('Tag', secondary=data_sets_tags,
                            backref=db.backref('data_sets', lazy='dynamic'))
    _urls = db.relationship('URL', backref='data_set', lazy='select')
    _batches = db.relationship('Batch', backref='data_set', lazy='dynamic')

    def __init__(self, data_collection_id, name, description, tags, urls):
        super(DataSet, self).__init__()
        self.data_collection_id = data_collection_id
        self._name = name
        self._description = description
        self._tags = tags
        self._urls = [URL(url, data_set_id=self.id) for url in urls]

    @hybrid_property
    def serialize(self):
        return {'Name': self.name,
                'Tags': [tag.name for tag in self.tags]}

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @hybrid_property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @hybrid_property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags.append(value)

    @hybrid_property
    def urls(self):
        return [url.url for url in self._urls]

    @urls.setter
    def urls(self, value):
        self._urls.append(URL(value, data_set_id=self.id))

    @hybrid_property
    def batches(self):
        return self._batches

    @batches.setter
    def batches(self, value):
        self._batches.append(value)


class Experiment(db.Model):
    """Represents an experiment composed of data collections and algorithms"""

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(64), index=True, unique=True)
    _description = db.Column(db.String(512), index=False, unique=False)

    # Relationships
    """
    Moving To Multi-User TODO:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """
    _tags = db.relationship('Tag', secondary=experiments_tags,
                            backref=db.backref('experiments', lazy='dynamic'))
    _algorithms = db.relationship('Algorithm',
                                  secondary=algorithms_experiments,
                                  backref=db.backref('experiments',
                                                     lazy='dynamic'))
    _collections = db.relationship('DataCollection',
                                   secondary=collections_experiments,
                                   backref=db.backref('experiments',
                                                      lazy='dynamic'))
    _batches = db.relationship('Batch', backref='experiment', lazy='dynamic')

    def __init__(self, name, description, tags, algorithms, collections):
        super(Experiment, self).__init__()
        self._name = name
        self._description = description
        self._tags = tags
        self._algorithms = algorithms
        self._collections = collections

    @hybrid_property
    def serialize(self):
        return {'Name': self.name,
                'Tags': [tag.name for tag in self.tags]}

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @hybrid_property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @hybrid_property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags.append(value)

    @hybrid_property
    def algorithms(self):
        return self._algorithms

    @algorithms.setter
    def algorithms(self, value):
        self._algorithms.append(value)

    @hybrid_property
    def collections(self):
        return self._collections

    @collections.setter
    def collections(self, value):
        self._collections.append(value)

    @hybrid_property
    def batches(self):
        return self._batches

    @batches.setter
    def batches(self, value):
        self._batches.append(value)


class Batch(db.Model):
    """Represents a batch of jobs to be deployed on HTCondor"""

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(64), index=True, unique=True)
    _description = db.Column(db.String(512), index=False, unique=False)
    _params = db.Column(db.PickleType(), index=False, unique=False)
    _memory = db.Column(db.Integer, index=False, unique=False)
    _disk = db.Column(db.Integer, index=False, unique=False)
    _flock = db.Column(db.Boolean(), index=False)
    _glide = db.Column(db.Boolean(), index=False)
    _arguments = db.Column(db.PickleType(), index=False, unique=False)
    _kwargs = db.Column(db.PickleType(), index=False, unique=False)
    _sweep = db.Column(db.String(64), index=False, unique=False)
    _wrapper = db.Column(db.String(64), index=False, unique=False)
    _submit_file = db.Column(db.String(64), index=False, unique=False)
    _params_file = db.Column(db.String(64), index=False, unique=False)
    _share_dir = db.Column(db.String(64), index=False, unique=False)
    _results_dir = db.Column(db.String(64), index=False, unique=False)
    _pre = db.Column(db.String(64), index=False, unique=False)
    _post = db.Column(db.String(64), index=False, unique=False)
    _job_pre = db.Column(db.String(64), index=False, unique=False)
    _job_post = db.Column(db.String(64), index=False, unique=False)
    _completed = db.Column(db.Boolean(), index=False)

    # Relationships
    """ TODO: Multi-User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'))
    data_set_id = db.Column(db.Integer, db.ForeignKey('data_set.id'))
    implementation_id = db.Column(db.Integer,
                                  db.ForeignKey('implementation.id'))
    _tags = db.relationship('Tag', secondary=batches_tags,
                            backref=db.backref('batches', lazy='dynamic'))
    _jobs = db.relationship('Job', backref='batch', lazy='select')

    def __init__(self,
                 experiment_id,
                 data_set_id,
                 implementation_id,
                 name,
                 description,
                 tags,
                 params,
                 memory,
                 disk,
                 flock,
                 glide,
                 arguments=None,
                 keyword_arguments=None,
                 sweep='sweep.dag',
                 wrapper='wrapper.sh',
                 submit_file='process.sub',
                 params_file='params.json',
                 share_directory='share',
                 results_directory='results',
                 pre_script=None,
                 job_pre_script=None,
                 post_script='batch_post.py',
                 job_post_script='job_post.py'):
        super(Batch, self).__init__()
        # Relationships
        self.experiment_id = experiment_id
        self.data_set_id = data_set_id
        self.implementation_id = implementation_id
        # Mandatory
        self._name = name
        self._description = description
        self._tags = tags
        self._params = params
        self._jobs = [Job(batch_id=self.id, uid=uid, params=job_params)
                      for uid, job_params in enumerate(params)]
        self._memory = memory
        self._disk = disk
        self._flock = flock
        self._glide = glide
        # Optional Arguments
        self._pre = pre_script
        self._post = post_script
        self._job_pre = job_pre_script
        self._job_post = job_post_script
        self._arguments = arguments
        self._kwargs = keyword_arguments
        self._sweep = sweep
        self._wrapper = wrapper
        self._submit_file = submit_file
        self._params_file = params_file
        self._share_dir = share_directory
        self._results_dir = results_directory
        self._completed = False

    def package(self):  # TODO: Remove after, replace zip if exists,
        """Packages the files to run a batch of jobs into a directory"""
        rootdir = makedir(
            os.path.join(current_app.config['STAGING_AREA'], self.safe_name))
        makedir(os.path.join(rootdir, self.results_dir))
        sharedir = makedir(os.path.join(rootdir, self.share_dir))
        self.write_template('sweep', os.path.join(rootdir, self.sweep))
        self.write_params(rootdir)
        self.write_template('wrapper', os.path.join(sharedir, self.wrapper))
        for job in self.jobs:  # Setup Job Directories
            job.package(rootdir)
        # self.write_template('batch_pre', os.path.join(sharedir, self.pre))
        self.write_template('batch_post', os.path.join(sharedir, self.post))
        # self.write_template('job_pre', os.path.join(sharedir, self.job_pre))
        self.write_template('job_post', os.path.join(sharedir, self.job_post))
        self.write_template('hack', os.path.join(sharedir, 'hack.sub'))
        shutil.copy(os.path.join(current_app.config['STAGING_AREA'], 'hack'),
                    sharedir)  # Copy fragile hack executable to share_dir
        zipfile = rootdir + '.zip'
        make_zipfile(zipfile, rootdir)
        shutil.rmtree(rootdir)  # clean up for next package
        return os.path.basename(zipfile)

    def write_params(self, rootdir):
        """ Writes a dictionary to a json file """
        filename = os.path.join(rootdir, self.params_file)
        with open(filename, 'w') as writefile:
            json.dump(self.params, writefile, sort_keys=True, indent=4)

    def write_template(self, template, filename):
        """ Renders a batch level tempalte and writes it to filename """
        if filename:
            with open(filename, 'w') as writefile:
                writefile.write(render_template(template, batch=self))

    @hybrid_property
    def serialize(self):
        return {'Name': self.name,
                'Tags': [tag.name for tag in self.tags]}

    @hybrid_property
    def mongoize(self):
        imp = Implementation.query.filter_by(id=self.implementation_id).first()
        exp = Experiment.query.filter_by(id=self.experiment_id).first()
        ds = DataSet.query.filter_by(id=self.data_set_id).first()
        dc = DataCollection.query.filter_by(id=ds.data_collection_id).first()
        alg = Algorithm.query.filter_by(id=imp._algorithm_id).first()
        return {'Batch': self.serialize,
                'Tags': [tag.name for tag in self.tags],  # TODO: conglomerate
                'Experiment': exp.serialize,
                'DataSet': ds.serialize,
                'DataCollection': dc.serialize,
                'Algorithm': alg.serialize,
                'Implementation': imp.serialize}

    @hybrid_property
    def safe_name(self):
        """Remove non-word characters & replace whitespace with underscore"""
        return re.sub(r"\s+", '_', re.sub(r"[^\w\s]", '', self.name))

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @hybrid_property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @hybrid_property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags.append(value)

    @hybrid_property
    def jobs(self):
        return self._jobs

    @jobs.setter
    def jobs(self, value):
        self._jobs.append(value)

    @hybrid_property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        self._params = yaml.load(value)  # TODO: Validate

    @hybrid_property
    def memory(self):
        return self._memory

    @memory.setter
    def memory(self, value):
        self._memory = value

    @hybrid_property
    def disk(self):
        return self._disk

    @disk.setter
    def disk(self, value):
        self._disk = value

    @hybrid_property
    def flock(self):
        return self._flock

    @flock.setter
    def flock(self, value):
        self._flock = value

    @hybrid_property
    def glide(self):
        return self._glide

    @hybrid_property
    def pre(self):
        return self._pre

    @pre.setter
    def pre(self, value):
        self._pre = value

    @hybrid_property
    def post(self):
        return self._post

    @post.setter
    def post(self, value):
        self._post = value

    @hybrid_property
    def job_pre(self):
        return self._job_pre

    @job_pre.setter
    def job_pre(self, value):
        self._job_pre = value

    @hybrid_property
    def job_post(self):
        return self._job_post

    @job_post.setter
    def job_post(self, value):
        self._job_post = value

    @hybrid_property
    def args(self):
        return self._arguments

    @args.setter
    def args(self, value):
        self._arguments = value

    @hybrid_property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        self._kwargs = value

    @hybrid_property
    def sweep(self):
        return self._sweep

    @sweep.setter
    def sweep(self, value):
        self._sweep = value

    @hybrid_property
    def wrapper(self):
        return self._wrapper

    @wrapper.setter
    def wrapper(self, value):
        self._wrapper = value

    @hybrid_property
    def submit_file(self):
        return self._submit_file

    @submit_file.setter
    def submit_file(self, value):
        self._submit_file = value

    @hybrid_property
    def params_file(self):
        return self._params_file

    @params_file.setter
    def params_file(self, value):
        self._params_file = value

    @hybrid_property
    def share_dir(self):
        return self._share_dir

    @share_dir.setter
    def share_dir(self, value):
        self._share_dir = value

    @hybrid_property
    def results_dir(self):
        return self._results_dir

    @results_dir.setter
    def results_dir(self, value):
        self._results_dir = value

    @hybrid_property
    def size(self):
        return len(self._jobs)

    @hybrid_property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, value):
        self._completed = value


class Job(db.Model):
    """Represents a single job, belonging to a Batch"""

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    _uid = db.Column(db.Integer, index=True, unique=False)
    _params = db.Column(db.PickleType(), index=True, unique=False)
    # Relationships
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'))
    """ TODO: Multi-User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """

    def __init__(self, batch_id, uid, params):
        super(Job, self).__init__()
        self.batch_id = batch_id
        self._uid = uid
        self._params = params

    def package(self, rootdir):
        """Packages files to run a job into a directory in rootdir"""
        jobdir = makedir(os.path.join(rootdir, self.uid))
        self.write_params(jobdir)
        self.write_template('process', os.path.join(jobdir, self.submit_file))
        self.write_template('subdag', os.path.join(jobdir, self.subdag))

    def write_params(self, jobdir):
        """ Writes a dictionary to a json file """
        filename = os.path.join(jobdir, self.params_file)
        with open(filename, 'w') as writefile:
            json.dump(self.params, writefile, sort_keys=True, indent=4)

    def write_template(self, template, filename):
        """ Renders a batch level tempalte and writes it to filename """
        if filename:
            with open(filename, 'w') as writefile:
                writefile.write(render_template(template, job=self))

    @hybrid_property
    def uid(self):
        return str(self._uid).zfill(len(str(self.batch.size-1)))

    @uid.setter
    def uid(self, value):
        self._uid = value

    @hybrid_property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        self._params = value

    @hybrid_property
    def params_file(self):
        return self.batch.params_file

    @hybrid_property
    def memory(self):
        return self.batch.memory

    @hybrid_property
    def disk(self):
        return self.batch.disk

    @hybrid_property
    def flock(self):
        return self.batch.flock

    @hybrid_property
    def glide(self):
        return self.batch.glide

    @hybrid_property
    def args(self):
        return self.batch.args

    @hybrid_property
    def kwargs(self):
        return self.batch.kwargs

    @hybrid_property
    def wrapper(self):
        return self.batch.wrapper

    @hybrid_property
    def submit_file(self):
        return self.batch.submit_file

    @hybrid_property
    def subdag(self):
        return self.uid + '.dag'

    @hybrid_property
    def share_dir(self):
        return self.batch.share_dir

    @hybrid_property
    def results_dir(self):
        return self.batch.results_dir

    @hybrid_property
    def pre(self):
        return self.batch.job_pre

    @hybrid_property
    def post(self):
        return self.batch.job_post

    @hybrid_property
    def batch_name(self):
        return self.batch.safe_name

    @hybrid_property
    def tags(self):
        return self.batch.tags


""" TODO: Parameter Validation
class Argument(db.Model):
    Entity representing a single valid argument
    belonging to an implementation of an algorithm

    # Fields
    id = db.Column(db.Integer,
                   primary_key=True)

    _name = db.Column(db.String(64),
                      index=True,
                      unique=True)

    _data_type = db.Column(db.Enum('int', 'float', 'string', 'enum'),
                           index=True,
                           unique=False)

    _optional = db.Column(db.Boolean(),
                          index=True)

    # Relationships
    implementation_id = db.Column(db.Integer,
                                  db.ForeignKey('implementation.id'))

    def __init__(self, implementation_id, name, data_type, optional):
        super(Argument, self).__init__()
        self.implementation_id = implementation_id
        self._name = name
        self._data_type = data_type
        self._optional = optional


    @hybrid_property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'data type': self.data_type,
                'optional': self.optional}

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @hybrid_property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        self._data_type = value

    @hybrid_property
    def optional(self):
        return self._optional

    @optional.setter
    def optional(self, value):
        self._optional = value
"""


class URL(db.Model):

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    _url = db.Column(db.String(124), index=False, unique=False)
    # Relationships
    data_set_id = db.Column(db.Integer, db.ForeignKey('data_set.id'))
    implementation_id = db.Column(db.Integer,
                                  db.ForeignKey('implementation.id'))

    def __init__(self, url, data_set_id=None, implementation_id=None):
        self._url = url
        self.data_set_id = data_set_id
        self.implementation_id = implementation_id

    @hybrid_property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value


# Universal Functions
def makedir(dirname):
    """ Creates a directory if it doesn't already exist """
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    return dirname


def make_zipfile(output_filename, source_dir):
    """http://stackoverflow.com/questions/1855095/"""
    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(output_filename, "w",
                         zipfile.ZIP_DEFLATED, True) as zip:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                os.chmod(filename, 0755)
                if os.path.isfile(filename):  # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zip.write(filename, arcname)
