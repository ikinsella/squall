from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

""" Tables For Many To Many Relationships """

ielinks = db.Table(
    'ielinks',
    db.Column(
        'implementation_id', db.Integer, db.ForeignKey('implementation.id')),
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id')))

delinks = db.Table(
    'delinks',
    db.Column('data_set_id', db.Integer, db.ForeignKey('data_set.id')),
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id')))

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
    db.Column(
        'implementation_id', db.Integer, db.ForeignKey('implementation.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

data_collections_tags = db.Table(
    'data_collections_tags',
    db.Column(
        'data_collection_id', db.Integer, db.ForeignKey('data_collection.id')),
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

jobs_tags = db.Table(
    'jobs_tags',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

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

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {username}>'.format(username=self.username)


class Algorithm(db.Model):
    """ Entity representing a single algorithm used in a an experiment
    """
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(512), index=False, unique=False)
    implementations = db.relationship(
        'Implementation', backref='algorithm', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.metadata = description

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


class Implementation(db.Model):
    """ Entity representing a single implementation of an algorithm
    """
    id = db.Column(db.Integer, primary_key=True)
    algorithm_id = db.Column(db.Integer, db.ForeignKey('algorithm.id'))

    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(512), index=False, unique=False)
    address = db.Column(db.String(256), index=False, unique=False)
    executable = db.Column(db.String(64), index=False, unique=False)

    arguments = db.relationship()

    def __init__(self, name, number, description):
        self.name = name
        self.number = number
        self.description = description

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


class Argument(db.Model):
    """Represents a single valid argument belonging to an
       implementation of an algorithm
    """
    def __init__(self, key, data_type, is_opitonal):
        super(Argument, self).__init__()
        self.key = key
        self.data_type = data_type
        self.is_opitonal = is_opitonal


class DataCollection(db.Model):
    """Represents a collection of datasets derived from a common source
    """
    def __init__(self, name, descipription, tags):
        super(DataCollection, self).__init__()
        self.name = name
        self.descipription = descipription
        self.tags = tags

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class DataSet(object):
    """Represents a single dataset belonging to a data collection
    """
    def __init__(self, name, address, description, tags):
        super(DataSet, self).__init__()
        self.name = name
        self.address = address
        self.description = description
        self.tags = tags

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Experiment(db.Model):
    """Represents an experiment composed jobs run with a variable number of
       datasets and algorithms
    """
    def __init__(self, name, description, tags):
        super(Experiment, self).__init__()
        self.name = name
        self.description = description
        self.tags = tags

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Batch(db.Model):
    """Represents a batch of jobs to be run on HTCondor
    """
    def __init__(self, params_list, num_jobs, description, tags):
        super(Batch, self).__init__()
        self.params_list = params_list
        self.num_jobs = num_jobs
        self.description = description
        self.tags = tags

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Job(db.Model):
    """Represents a single job, belonging to a Batch
    """
    def __init__(self, process_number):
        super(Job, self).__init__()
        self.process_number = process_number

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Param(db.Model):
    """Represents a single parameter value belonging to a job
    """
    def __init__(self, key, value):
        super(Param, self).__init__()
        self.key = key
        self.value = value

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Tag(db.Model):
    """ Represents a tag which is used to add query-able meta data
        to experiments, batches, data collections, data sets, algorithms,
        and implementations. A User defines tags in a view and each collected
        job is associated with all the tags contained in its hierarchy.
    """
    def __init__(self, value):
        super(Tag, self).__init__()
        self.value = value
