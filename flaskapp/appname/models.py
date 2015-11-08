from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()


""" Tables For Many To Many Relationships """

# not currently in use
implementations_experiments = db.Table(
    'implementations_experiments',
    db.Column('implementation_id', db.Integer, db.ForeignKey('implementation.id')),
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
    db.Column('collection_id', db.Integer, db.ForeignKey('data_collection.id')))

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
    db.Column('implementation_id', db.Integer, db.ForeignKey('implementation.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

data_collections_tags = db.Table(
    'data_collections_tags',
    db.Column('data_collection_id', db.Integer, db.ForeignKey('data_collection.id')),
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
    db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
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
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

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
    @property
    def serialize(self):
	return {
		'id'         : self.id,
		'name'       : self.name,
		'description': self.description
	}
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @property
    def serialize(self):
	return {
		'id'         : self.id,
		'name'       : self.name,
		'description': self.description
	}

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

#    def set_decription(self, description):
#        self.description = description
#
#    def set_name(self, name):
#        self.name = name
#
#    def get_metadata(self):
#        return self.description
#
#    def get_name(self):
#        return self.name
#
#    def get_id(self):
#        try:
#            return unicode(self.id)  # python 2
#        except NameError:
#            return str(self.id)  # python 3
#

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
        return {
		'id'         : self.id,
		'name'       : self.name,
		'address'    : self.address, 
		'executable' : self.executable,
		'description': self.description
	}

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
       return {
		'id'       : self.id,
		'name'     : self.name,
		'data type': self.data_type,
		'optional' : self.optional
	}

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
	return {
		'id'         : self.id,
		'name'       : self.name,
		'description': self.description
	}

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

    @property
    def serialize(self):
	return {
		'id'         : self.id,
		'name'       : self.name,
		'address'    : self.address,
		'description': self.description	
	}

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

    @property
    def serialize(self):
	return {
		'id'         : self.id,
		'name'       : self.name,
		'description': self.description
	}


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

    name = db.Column(db.String(64),
                     index=True,
                     unique=True)

    description = db.Column(db.String(512),
                            index=False,
                            unique=False)

    # Relationships

    experiment_id = db.Column(db.Integer,
                              db.ForeignKey('experiment.id'))

    data_set_id = db.Column(db.Integer,
                            db.ForeignKey('data_set.id'))

    implementation_id = db.Column(db.Integer,
                                  db.ForeignKey('implementation.id'))

    jobs = db.relationship('Job',
                           backref='batch',
                           lazy='dynamic')

    tags = db.relationship('Tag',
                           secondary=batches_tags,
                           backref=db.backref('batches',
                                              lazy='dynamic'))
    """
    Moving To Multi-User TODO:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """

    def __init__(self, name, description, experiment_id, data_set_id, implementation_id):
        super(Batch, self).__init__()
        self.name = name
        self.description = description
        self.experiment_id = experiment_id
        self.data_set_id = data_set_id
        self.implementation_id = implementation_id

    @property
    def serialize(self):
	return {
		'id'         : self.id,
		'name'       : self.name,
		'description': self.description
	}
	

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
    def experiment_idx(self):
       return self.experiment_id
    @experiment_idx.setter
    def experiment_idx(self, value):
       self.experiment_id = value
    @hybrid_property
    def data_set_idx(self):
       return self.data_set_id
    @data_set_idx.setter
    def data_set_idx(self, value):
       self.data_set_id = value
    @hybrid_property
    def implementation_idx(self):
       return self.implementation_id
    @implementation_idx.setter
    def implementation_idx(self, value):
       self.implementation_id = value
    @hybrid_property
    def jobsx(self):
       return self.jobs
    @jobsx.setter
    def jobsx(self, value):
       self.jobs.append(value)
    @hybrid_property
    def tagsx(self):
       return self.tags
    @tagsx.setter
    def tagsx(self, value):
       self.tags.append(value)

class Job(db.Model):
    """Represents a single job, belonging to a Batch
    """

    # Fields

    id = db.Column(db.Integer,
                   primary_key=True)

    is_completed = db.Column(db.Boolean,
                             index=True,
                             unique=False)

    process = db.Column(db.Integer,
                        index=True,
                        unique=True)

    # Relationships

    batch_id = db.Column(db.Integer,
                         db.ForeignKey('batch.id'))

    params = db.relationship('Param',
                             backref='job',
                             lazy='dynamic')

    tags = db.relationship('Tag',
                           secondary=jobs_tags,
                           backref=db.backref('jobs',
                                              lazy='dynamic'))
    """
    Moving To Multi-User TODO:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """

    def __init__(self, process):
        super(Job, self).__init__()
        self.process = process
        self.is_completed = False

    @property
    def serialize(self):
	return {
		'id'         : self.id,
		'is complete': self.is_complete,
		'process'    : self.process
	}


    @hybrid_property
    def is_completedx(self):
       return self.is_completed
    @is_completedx.setter 
    def is_completedx(self, value):
       self.is_completed = value    
    @hybrid_property
    def processx(self):
       return self.process
    @processx.setter 
    def processx(self, value):
       self.process = value     
    @hybrid_property
    def idx(self):
       return self.id
    @idx.setter 
    def idx(self, value):
       self.id = value    
    @hybrid_property
    def batch_idx(self):
       return self.batch_id
    @batch_idx.setter
    def batch_idx(self, value):
       self.batch_id = value
    @hybrid_property
    def paramsx(self):
       return self.params
    @paramsx.setter
    def paramsx(self, value):
       self.params.append(value)
    @hybrid_property
    def tagsx(self):
       return self.tags
    @tagsx.setter
    def tagsx(self, value):
       self.tags.append(value)

class Param(db.Model):
    """ Represents a single parameter value belonging to a job
    """

    # Fields

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(64),
                     index=True,
                     unique=True)

    # TODO: make value data-type flexible
    value = db.Column(db.String(64),
                      index=True,
                      unique=True)

    # Relationships

    job_id = db.Column(db.Integer,
                       db.ForeignKey('job.id'))

    def __init__(self, name, value):
        super(Param, self).__init__()
        self.name = name
        self.value = value

    @property
    def serialize(self):
	return {
		'id'  : self.id,
		'name': self.name
	}

    @hybrid_property
    def namex(self):
       return self.name
    @namex.setter 
    def namex(self, value):
       self.name = value    
    @hybrid_property
    def idx(self):
       return self.id
    @idx.setter 
    def idx(self, value):
       self.id = value    
    @hybrid_property
    def job_idx(self):
       return self.job_id
    @job_idx.setter
    def job_idx(self, value):
       self.job_id = value

class Tag(db.Model):
    """ Represents a tag which is used to add query-able meta data
        to experiments, batches, data collections, data sets, algorithms,
        and implementations. A User defines tags in a view and each collected
        job is associated with all the tags contained in its hierarchy.
    """

    # Fields

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(64),
                     index=True,
                     unique=True)

    # Relationships
    """
    Moving To Multi-User TODO:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """

    def __init__(self, name):
        super(Tag, self).__init__()
        self.name = name

    @property
    def serialize(self):
	return {
		'id'  : self.id,
		'name': self.name
	}

    @hybrid_property
    def namex(self):
       return self.name
    @namex.setter 
    def namex(self, value):
       self.name = value    
    @hybrid_property
    def idx(self):
       return self.id
    @idx.setter 
    def idx(self, value):
       self.id = value    
    @hybrid_property
    def user_idx(self):
       return self.user_id
    @user_idx.setter
    def user_idx(self, value):
       self.user_id = value
