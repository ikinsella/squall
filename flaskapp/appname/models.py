import os
import yaml
import json
import copy
import numpy as np

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()


""" Tables For Many To Many Relationships """

# not currently in use
implementations_experiments = db.Table(
    'implementations_experiments',
    db.Column('implementation_id', db.Integer,
              db.ForeignKey('implementation.id')),
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id')))

# not currently in use
data_sets_experiments = db.Table(
    'data_sets_experiments',
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id')),
    db.Column('data_set_id', db.Integer, db.ForeignKey('data_set.id')))

# Elliott added
collections_experiments = db.Table(
    'collections_experiments',
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id')),
    db.Column('collection_id', db.Integer,
              db.ForeignKey('data_collection.id')))

# Elliott added
algorithms_experiments = db.Table(
    'algorithms_experiments',
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id')),
    db.Column('algorithm_id', db.Integer, db.ForeignKey('algorithm.id')))

users_tags = db.Table(
    'users_tags',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

algorithms_tags = db.Table(
    'algorithms_tags',
    db.Column('algorithm_id', db.Integer, db.ForeignKey('algorithm.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

implementations_tags = db.Table(
    'implementations_tags',
    db.Column('implementation_id', db.Integer,
              db.ForeignKey('implementation.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

data_collections_tags = db.Table(
    'data_collections_tags',
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
    """ Represents a single User who has access to the application
    """

    # Fields
    id = db.Column(db.Integer(),
                   primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    tags = db.relationship('Tag', secondary=users_tags,
                           backref=db.backref('users',
                                              lazy='dynamic'))
    # relationships
    """
    Moving To Multi-User TODO:
    algorithms = db.relationship()
    datacollections = db.relationship()
    experiments = db.relationship()
    batches = db.relationship()
    tags = db.relationship()
    """

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

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

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def get_id(self):
        return self.id

    @hybrid_property
    def usernamex(self):
        return self.username

    @usernamex.setter
    def usernamex(self, value):
        self.username = value

    @hybrid_property
    def passwordx(self):
        return self.password

    @passwordx.setter
    def passwordx(self, value):
        self.password = generate_password_hash(value)

    @hybrid_property
    def idx(self):
        return self.id

    @idx.setter
    def idx(self, value):
        self.id = value

    def __repr__(self):
        return '<User {username}>'.format(username=self.username)


class Algorithm(db.Model):
    """ Entity representing a single algorithm used in a an experiment
    """

    # Fields

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(64),
                     index=True,
                     unique=True)

    description = db.Column(db.String(512),
                            index=False,
                            unique=False)

    # Relationships

    implementations = db.relationship('Implementation',
                                      backref='algorithm',
                                      lazy='dynamic')
    tags = db.relationship('Tag',
                           secondary=algorithms_tags,
                           backref=db.backref('algorithms',
                                              lazy='dynamic'))
    """
    Moving To Multi-User TODO:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description}

    def set_decription(self, description):
        self.description = description

    def set_name(self, name):
        self.name = name

    def get_metadata(self):
        return self.description

    def get_name(self):
        return self.name

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @hybrid_property
    def namex(self):
        return self.name

    @namex.setter
    def namex(self, value):
        self.name = value

    @hybrid_property
    def descriptionx(self):
        return self.description

    @descriptionx.setter
    def descriptionx(self, value):
        self.description = value

    @hybrid_property
    def idx(self):
        return self.id

    @idx.setter
    def idx(self, value):
        self.id = value

    @hybrid_property
    def implementationsx(self):
        return self.implementations

    @implementationsx.setter
    def implementationsx(self, value):
        self.implementations.append(value)

    @hybrid_property
    def tagsx(self):
        return self.tags

    @tagsx.setter
    def tagsx(self, value):
        self.tags.append(value)


class Implementation(db.Model):
    """ Entity representing a single implementation of an algorithm
    """

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.String(256), index=False, unique=False)
    executable = db.Column(db.String(64), index=False, unique=False)
    description = db.Column(db.String(512), index=False, unique=False)

    # Relationships

    algorithm_id = db.Column(db.Integer,
                             db.ForeignKey('algorithm.id'))

    arguments = db.relationship('Argument',
                                backref='implementation',
                                lazy='dynamic')

    batches = db.relationship('Batch',
                              backref='implementation',
                              lazy='dynamic')

    tags = db.relationship('Tag',
                           secondary=implementations_tags,
                           backref=db.backref('implementations',
                                              lazy='dynamic'))

    """
    Moving To Multi-User TODO:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """

    def __init__(self, name, address, executable, description, algorithm_id):
        self.name = name
        self.address = address
        self.executable = executable
        self.description = description
        self.algorithm_id = algorithm_id

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'address': self.address,
                'executable': self.executable,
                'description': self.description}

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @hybrid_property
    def namex(self):
        return self.name

    @namex.setter
    def namex(self, value):
        self.name = value

    @hybrid_property
    def descriptionx(self):
        return self.description

    @descriptionx.setter
    def descriptionx(self, value):
        self.description = value

    @hybrid_property
    def idx(self):
        return self.id

    @idx.setter
    def idx(self, value):
        self.id = value

    @hybrid_property
    def addressx(self):
        return self.address

    @addressx.setter
    def addressx(self, value):
        self.address = value

    @hybrid_property
    def executablex(self):
        return self.executable

    @executablex.setter
    def executablex(self, value):
        self.executable = value

    @hybrid_property
    def algorithm_idx(self):
        return self.algorithm_id

    @algorithm_idx.setter
    def algorithm_idx(self, value):
        self.algorithm_id = value

    @hybrid_property
    def argumentsx(self):
        return self.arguments

    @argumentsx.setter
    def argumentsx(self, value):
        self.arguments.append(value)

    @hybrid_property
    def batchesx(self):
        return self.batches

    @batchesx.setter
    def batchesx(self, value):
        self.batches.append(value)

    @hybrid_property
    def tagsx(self):
        return self.tags

    @tagsx.setter
    def tagsx(self, value):
        self.tags.append(value)


class Argument(db.Model):
    """ Entity representing a single valid argument belonging to an
        implementation of an algorithm
    """

    # Fields

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(64),
                     index=True,
                     unique=True)

    data_type = db.Column(db.Enum('int', 'float', 'string', 'enum'),
                          index=True,
                          unique=False)

    optional = db.Column(db.Boolean(),
                         index=True)

    # Relationships
    implementation_id = db.Column(db.Integer,
                                  db.ForeignKey('implementation.id'))

    def __init__(self, name, data_type, optional):
        super(Argument, self).__init__()
        self.name = name
        self.data_type = data_type
        self.optional = optional

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'data type': self.data_type,
                'optional': self.optional}

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @hybrid_property
    def namex(self):
        return self.name

    @namex.setter
    def namex(self, value):
        self.name = value

    @hybrid_property
    def data_typex(self):
        return self.data_type

    @data_typex.setter
    def data_typex(self, value):
        self.data_type = value

    @hybrid_property
    def idx(self):
        return self.id

    @idx.setter
    def idx(self, value):
        self.id = value

    @hybrid_property
    def optionalx(self):
        return self.optional

    @optionalx.setter
    def optionalx(self, value):
        self.optional = value

    @hybrid_property
    def implementation_idx(self):
        return self.implementation_id

    @implementation_idx.setter
    def implementation_idx(self, value):
        self.implementation_id = value


class DataCollection(db.Model):
    """ Represents a collection of datasets derived from a common source
    """

    # Fields

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(64),
                     index=True,
                     unique=True)

    description = db.Column(db.String(512),
                            index=False,
                            unique=False)

    # Relationships

    data_sets = db.relationship('DataSet',
                                backref='data_collection',
                                lazy='dynamic')

    tags = db.relationship('Tag',
                           secondary=data_collections_tags,
                           backref=db.backref('data_collections',
                                              lazy='dynamic'))

    """
    Moving To Multi-User TODO:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """

    def __init__(self, name, description):
        super(DataCollection, self).__init__()
        self.name = name
        self.description = description

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description}

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @hybrid_property
    def namex(self):
        return self.name

    @namex.setter
    def namex(self, value):
        self.name = value

    @hybrid_property
    def descriptionx(self):
        return self.description

    @descriptionx.setter
    def descriptionx(self, value):
        self.description = value

    @hybrid_property
    def idx(self):
        return self.id

    @idx.setter
    def idx(self, value):
        self.id = value

    @hybrid_property
    def data_setsx(self):
        return self.data_sets

    @data_setsx.setter
    def data_setsx(self, value):
        self.data_sets.append(value)

    @hybrid_property
    def tagsx(self):
        return self.tags

    @tagsx.setter
    def tagsx(self, value):
        self.tags.append(value)


class DataSet(db.Model):
    """ Represents a single dataset belonging to a data collection
    """

    # Fields

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(64),
                     index=True,
                     unique=True)

    address = db.Column(db.String(256),
                        index=False,
                        unique=False)

    description = db.Column(db.String(512),
                            index=False,
                            unique=False)

    # Relationships
    data_collection_id = db.Column(
        db.Integer, db.ForeignKey('data_collection.id'))

    batches = db.relationship('Batch',
                              backref='data_set',
                              lazy='dynamic')

    tags = db.relationship('Tag',
                           secondary=data_sets_tags,
                           backref=db.backref('data_sets',
                                              lazy='dynamic'))

    """
    Moving To Multi-User TODO:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """

    def __init__(self, name, address, description, data_collection_id):
        super(DataSet, self).__init__()
        self.name = name
        self.address = address
        self.description = description
        self.data_collection_id = data_collection_id

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'address': self.address,
                'description': self.description}

    @hybrid_property
    def namex(self):
        return self.name

    @namex.setter
    def namex(self, value):
        self.name = value

    @hybrid_property
    def descriptionx(self):
        return self.description

    @descriptionx.setter
    def descriptionx(self, value):
        self.description = value

    @hybrid_property
    def idx(self):
        return self.id

    @idx.setter
    def idx(self, value):
        self.id = value

    @hybrid_property
    def addressx(self):
        return self.address

    @addressx.setter
    def addressx(self, value):
        self.address = value

    @hybrid_property
    def data_collection_idx(self):
        return self.data_collection_id

    @data_collection_idx.setter
    def data_collection_idx(self, value):
        self.data_collection_id = value

    @hybrid_property
    def batchesx(self):
        return self.batches

    @batchesx.setter
    def batchesx(self, value):
        self.batches.append(value)

    @hybrid_property
    def tagsx(self):
        return self.tags

    @tagsx.setter
    def tagsx(self, value):
        self.tags.append(value)


class Experiment(db.Model):
    """Represents an experiment composed jobs run with a variable number of
       datasets and algorithms
    """

    # Fields

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(64),
                     index=True,
                     unique=True)

    description = db.Column(db.String(512), index=False, unique=False)

    # Relationships

    # not currently in use
    data_sets = db.relationship('DataSet',
                                secondary=data_sets_experiments,
                                backref=db.backref('experiments',
                                                   lazy='dynamic'))
    # not currently in use
    implementations = db.relationship('Implementation',
                                      secondary=implementations_experiments,
                                      backref=db.backref('experiments',
                                                         lazy='dynamic'))

    # Elliott added
    collections = db.relationship('DataCollection',
                                  secondary=collections_experiments,
                                  backref=db.backref('experiments',
                                                     lazy='dynamic'))

    # Elliott added
    algorithms = db.relationship('Algorithm',
                                 secondary=algorithms_experiments,
                                 backref=db.backref('experiments',
                                                    lazy='dynamic'))

    batches = db.relationship('Batch',
                              backref='experiment',
                              lazy='dynamic')

    tags = db.relationship('Tag',
                           secondary=experiments_tags,
                           backref=db.backref('experiments',
                                              lazy='dynamic'))
    """
    Moving To Multi-User TODO:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """

    def __init__(self, name, description):
        super(Experiment, self).__init__()
        self.name = name
        self.description = description

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description}

    @hybrid_property
    def namex(self):
        return self.name

    @namex.setter
    def namex(self, value):
        self.name = value

    @hybrid_property
    def descriptionx(self):
        return self.description

    @descriptionx.setter
    def descriptionx(self, value):
        self.description = value

    @hybrid_property
    def idx(self):
        return self.id

    @idx.setter
    def idx(self, value):
        self.id = value

    @hybrid_property
    def data_setsx(self):
        return self.data_sets

    @data_setsx.setter
    def data_setsx(self, value):
        self.data_sets.append(value)

    @hybrid_property
    def implementationsx(self):
        return self.implementations

    @implementationsx.setter
    def implementationsx(self, value):
        self.implementations.append(value)

    @hybrid_property
    def batchesx(self):
        return self.batches

    @batchesx.setter
    def batchesx(self, value):
        self.batches.append(value)

    @hybrid_property
    def tagsx(self):
        return self.tags

    @tagsx.setter
    def tagsx(self, value):
        self.tags.append(value)


class Batch(db.Model):
    """ Represents a batch of jobs to be run on HTCondor
    """

    # Fields

    id = db.Column(db.Integer,
                   primary_key=True)

    _name = db.Column(db.String(64),
                      index=True,
                      unique=True)

    _description = db.Column(db.String(512),
                             index=False,
                             unique=False)

    # Relationships

    experiment_id = db.Column(db.Integer,
                              db.ForeignKey('experiment.id'))

    data_set_id = db.Column(db.Integer,
                            db.ForeignKey('data_set.id'))

    implementation_id = db.Column(db.Integer,
                                  db.ForeignKey('implementation.id'))

    _jobs = db.relationship('Job',
                            backref='batch',
                            lazy='dynamic')

    _tags = db.relationship('Tag',
                            secondary=batches_tags,
                            backref=db.backref('batches',
                                               lazy='dynamic'))
    """
    Moving To Multi-User TODO:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """

    # TODO
    def __init__(self,
                 name,
                 description,
                 experiment_id,
                 data_set_id,
                 implementation_id,
                 params,
                 memory,
                 disk,
                 flock,
                 glide,
                 arguments=None,
                 keyword_arguments=None,
                 setup_scripts=None,
                 sweep='sweep.dag',
                 wrapper='wrapper.sh',
                 submit_file='process.sub',
                 params_file='params.json',
                 share_directory='share',
                 pre_script=None,
                 job_pre_script=None,
                 post_script='batch_post.py',
                 job_post_script='job_post.py'):
        super(Batch, self).__init__()
        """ Assign Fields """
        # Relationships
        self.experiment_id = experiment_id
        self.data_set_id = data_set_id
        self.implementation_id = implementation_id
        # Mandatory
        self._name = name
        self._description = description
        self._params = params
        self._memory = memory  # Marked Share
        self._disk = disk  # Marked Share
        self._flock = flock
        self._glide = glide
        # Optional Arguments
        self._args = arguments  # Marked Share
        self._kwargs = keyword_arguments  # Marked Share
        self._setup_scripts = setup_scripts
        self._sweep = sweep
        self._wrapper = wrapper  # Marked Share
        self._submit_file = submit_file  # Marked Share
        self._share_dir = share_directory  # Marked Share
        self._pre = pre_script
        self._post = post_script
        self._job_pre = job_pre_script  # Marked Share
        self._job_post = job_post_script  # Marked Share

        """ Make Jobs """
        enum_params = self._enumerate_params()
        self.size = len(enum_params)  # Replace With Func
        self.jobs = [Job(batch_id=self.id, uid=uid, params=enum_param)
                     for uid, enum_param in enumerate(enum_params)]

    def _enumerate_params(self):
        """ Expands Yaml Fields List Of Param Files For Each Job"""

        try:  # If Expand Fields Doesn't Exist, Nothing To Be Done
            expand_fields = self.params['ExpandFields']
            del self.params['ExpandFields']
        except KeyError:
            return self.params

        # Copy Only Static Fields
        static_data = copy.copy(self.params)
        for field in [key for key in expand_fields]:
            del static_data[field]

        # Count Number Of Values Per Expand Field
        field_lengths = np.zeros(len(expand_fields))
        for idx, field in enumerate(expand_fields):
            if isinstance(field, list) or isinstance(field, tuple):
                subfields = [len(self.params[key]) for key in field]
                if not all(map(lambda x: x is subfields[0], subfields)):
                    raise RuntimeError('Incompatible Length: ExpandFields')
                field_lengths[idx] = len(subfields[0])
            else:
                field_lengths[idx] = len(self.params[field])

        enum_params = [static_data for _ in xrange(int(field_lengths.prod()))]

        # Enumerate Expand Fields
        for cdx, enum_param in enumerate(enum_params):
            for idx, field in zip(
                    np.unravel_index(cdx, field_lengths), expand_fields):
                if isinstance(field, list) or isinstance(field, tuple):
                    for k in field:
                        enum_param[k] = self.params[k][idx]
                    else:
                        enum_param[field] = self.params[field][idx]
        return enum_params

    def _create_jobs(self, enum_params):
        """ Creates Jobs Associated With Batch From Enumerated Parameters """

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @property
    def serialize(self):
        serial_jobs = [job.serialize for job in self.jobs]  # Make dict
        serial_tags = [tag.serialize for tag in self.tags]  # Propogate
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'params': self.params,
                'memory': self.memory,
                'disk': self.disk,
                'flock': self.flock,
                'glide': self.glide,
                'tags': serial_tags,
                'jobs': serial_jobs,
                'args': self.args,
                'kwargs': self.kwargs,
                'sweep': self.sweep,
                'setup_scripts': self.setup_scripts,
                'wrapper': self.wrapper,
                'submit_file': self.submit_file,
                'share_dir': self.share_dir,
                'pre': self.pre,
                'post': self.post,
                'job_pre': self.job_pre,
                'job_post': self.job_post}

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
    def jobs(self):
        return self._jobs

    @jobs.setter
    def jobs(self, value):
        self._jobs.append(value)

    @hybrid_property
    def tags(self):  # TODO propogate
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags.append(value)

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
    def args(self):
        return self.batch.args

    @args.setter
    def args(self, value):
        self._args = value

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
    def setup_scripts(self):
        return self._setup_scripts

    @setup_scripts.setter
    def setup_scripts(self, value):
        self._setup_scripts.append(value)

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
    def share_dir(self):
        return self._share_dir

    @share_dir.setter
    def share_dir(self, value):
        self._share_dir = value

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
    def pre(self):
        return self._job_pre

    @pre.setter
    def pre(self, value):
        self._job_pre = value

    @hybrid_property
    def job_pre(self, value):
        self._job_pre = value

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
    def exe(self):
        return self.implementation.executable

    @hybrid_property
    def code_urls(self):
        return self.implementation.url

    @hybrid_property
    def data_urls(self):
        return self.data_set.url

    @hybrid_property
    def size(self):
        return len(self._jobs)


class Job(db.Model):
    """Represents a single job, belonging to a Batch
    """

    # Fields

    id = db.Column(db.Integer,
                   primary_key=True)

    _uid = db.Column(db.Integer,
                     index=True,
                     unique=True)

    # Relationships

    batch_id = db.Column(db.Integer,
                         db.ForeignKey('batch.id'))

    """
    Moving To Multi-User TODO:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """

    def __init__(self,
                 batch_id,
                 uid,
                 params):
        super(Job, self).__init__()
        self.batch_id = batch_id
        self._params = params
        self._uid = str(uid).zfill(len(str(self.batch.size-1)))

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @hybrid_property
    def serialize(self):
        return {'id': self.id,
                'uid': self.uid,
                'params': self.params}

    @hybrid_property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = str(value).zfill(len(str(self.batch.size-1)))

    @hybrid_property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        self._params = value

    @hybrid_property
    def exe(self):
        return self.batch.exe

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
    def share_dir(self):
        return self.batch.share_dir

    @hybrid_property
    def pre(self):
        return self.batch.job_pre

    @hybrid_property
    def post(self):
        return self.batch.job_post

    @hybrid_property
    def tags(self):
        return self.batch.tags


class Param(db.Model):
    """ Represents a single parameter value belonging to a job
    """

    # Fields

    id = db.Column(db.Integer,
                   primary_key=True)

    _name = db.Column(db.String(64),
                      index=True,
                      unique=True)

    # TODO: make value enumerated instead of string
    _data_type = db.Column(db.String(64),
                           index=True,
                           unique=True)

    # Relationships
    # Add relationship to a particular implemetation

    def __init__(self, name, data_type):
        super(Param, self).__init__()
        self._name = name
        self._data_type = data_type

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name}

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


class Tag(db.Model):
    """ Represents a tag which is used to add query-able meta data
        to experiments, batches, data collections, data sets, algorithms,
        and implementations. A User defines tags in a view and each collected
        job is associated with all the tags contained in its hierarchy.
    """

    # Fields

    id = db.Column(db.Integer,
                   primary_key=True)

    _name = db.Column(db.String(64),
                      index=True,
                      unique=True)

    # Relationships
    """
    Moving To Multi-User TODO:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """

    def __init__(self, name):
        super(Tag, self).__init__()
        self._name = name

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self._name}

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class Result(db.Model):

    # fields

    id = db.Column(db.Integer,
                   primary_key=True)
    batch_id = db.Column(db.Integer,
                         index=True,
                         unique=True)
    _blob = db.Column(db.LargeBinary,
                      index=True,
                      unique=True)
    # relationships
    # none for now?

    def __init__(self, batch_id, blob):
        self.batch_id = batch_id
        self._blob = blob

    # properties

    @hybrid_property
    def blob(self):
        return self._blob

    @blob.setter
    def blobx(self, value):
        self._blob = value
