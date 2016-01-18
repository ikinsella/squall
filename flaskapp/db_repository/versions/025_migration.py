from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
argument = Table('argument', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('data_type', VARCHAR(length=6)),
    Column('optional', BOOLEAN),
    Column('implementation_id', INTEGER),
)

data_collections_tags = Table('data_collections_tags', pre_meta,
    Column('data_collection_id', INTEGER),
    Column('tag_id', INTEGER),
)

data_sets_experiments = Table('data_sets_experiments', pre_meta,
    Column('experiment_id', INTEGER),
    Column('data_set_id', INTEGER),
)

implementations_experiments = Table('implementations_experiments', pre_meta,
    Column('implementation_id', INTEGER),
    Column('experiment_id', INTEGER),
)

jobs_tags = Table('jobs_tags', pre_meta,
    Column('job_id', INTEGER),
    Column('tag_id', INTEGER),
)

param = Table('param', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('value', VARCHAR(length=64)),
    Column('job_id', INTEGER),
)

users_tags = Table('users_tags', pre_meta,
    Column('user_id', INTEGER),
    Column('tag_id', INTEGER),
)

collections_tags = Table('collections_tags', post_meta,
    Column('data_collection_id', Integer),
    Column('tag_id', Integer),
)

data_collection = Table('data_collection', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('description', VARCHAR(length=512)),
)

data_collection = Table('data_collection', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('_name', String(length=64)),
    Column('_description', String(length=512)),
)

algorithm = Table('algorithm', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('description', VARCHAR(length=512)),
)

algorithm = Table('algorithm', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('_name', String(length=64)),
    Column('_description', String(length=512)),
)

implementation = Table('implementation', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('address', VARCHAR(length=256)),
    Column('executable', VARCHAR(length=64)),
    Column('description', VARCHAR(length=512)),
    Column('algorithm_id', INTEGER),
)

implementation = Table('implementation', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('_name', String(length=64)),
    Column('_description', String(length=512)),
    Column('_urls', PickleType),
    Column('_setup_scripts', PickleType),
    Column('_executable', String(length=64)),
    Column('_algorithm_id', Integer),
)

data_set = Table('data_set', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('address', VARCHAR(length=256)),
    Column('description', VARCHAR(length=512)),
    Column('data_collection_id', INTEGER),
)

data_set = Table('data_set', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('_name', String(length=64)),
    Column('_description', String(length=512)),
    Column('_urls', PickleType),
    Column('data_collection_id', Integer),
)

tag = Table('tag', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
)

tag = Table('tag', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('_name', String(length=64)),
)

batch = Table('batch', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('description', VARCHAR(length=512)),
    Column('experiment_id', INTEGER),
    Column('data_set_id', INTEGER),
    Column('implementation_id', INTEGER),
)

batch = Table('batch', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('_name', String(length=64)),
    Column('_description', String(length=512)),
    Column('_params', PickleType),
    Column('_memory', Integer),
    Column('_disk', Integer),
    Column('_flock', Boolean),
    Column('_glide', Boolean),
    Column('_arguments', PickleType),
    Column('_kwargs', PickleType),
    Column('_sweep', String(length=64)),
    Column('_submit_file', String(length=64)),
    Column('_params_file', String(length=64)),
    Column('_share_dir', String(length=64)),
    Column('_pre', String(length=64)),
    Column('_post', String(length=64)),
    Column('_job_pre', String(length=64)),
    Column('_job_post', String(length=64)),
    Column('experiment_id', Integer),
    Column('data_set_id', Integer),
    Column('implementation_id', Integer),
)

job = Table('job', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('is_completed', BOOLEAN),
    Column('process', INTEGER),
    Column('batch_id', INTEGER),
)

job = Table('job', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('_uid', Integer),
    Column('batch_id', Integer),
)

experiment = Table('experiment', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('description', VARCHAR(length=512)),
)

experiment = Table('experiment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('_name', String(length=64)),
    Column('_description', String(length=512)),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=64)),
    Column('password', VARCHAR(length=64)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('_username', String(length=64)),
    Column('_password', String(length=64)),
)

result = Table('result', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('batch_id', INTEGER),
    Column('blob', BLOB),
)

result = Table('result', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('batch_id', Integer),
    Column('_blob', PickleType),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['argument'].drop()
    pre_meta.tables['data_collections_tags'].drop()
    pre_meta.tables['data_sets_experiments'].drop()
    pre_meta.tables['implementations_experiments'].drop()
    pre_meta.tables['jobs_tags'].drop()
    pre_meta.tables['param'].drop()
    pre_meta.tables['users_tags'].drop()
    post_meta.tables['collections_tags'].create()
    pre_meta.tables['data_collection'].columns['description'].drop()
    pre_meta.tables['data_collection'].columns['name'].drop()
    post_meta.tables['data_collection'].columns['_description'].create()
    post_meta.tables['data_collection'].columns['_name'].create()
    pre_meta.tables['algorithm'].columns['description'].drop()
    pre_meta.tables['algorithm'].columns['name'].drop()
    post_meta.tables['algorithm'].columns['_description'].create()
    post_meta.tables['algorithm'].columns['_name'].create()
    pre_meta.tables['implementation'].columns['address'].drop()
    pre_meta.tables['implementation'].columns['algorithm_id'].drop()
    pre_meta.tables['implementation'].columns['description'].drop()
    pre_meta.tables['implementation'].columns['executable'].drop()
    pre_meta.tables['implementation'].columns['name'].drop()
    post_meta.tables['implementation'].columns['_algorithm_id'].create()
    post_meta.tables['implementation'].columns['_description'].create()
    post_meta.tables['implementation'].columns['_executable'].create()
    post_meta.tables['implementation'].columns['_name'].create()
    post_meta.tables['implementation'].columns['_setup_scripts'].create()
    post_meta.tables['implementation'].columns['_urls'].create()
    pre_meta.tables['data_set'].columns['address'].drop()
    pre_meta.tables['data_set'].columns['description'].drop()
    pre_meta.tables['data_set'].columns['name'].drop()
    post_meta.tables['data_set'].columns['_description'].create()
    post_meta.tables['data_set'].columns['_name'].create()
    post_meta.tables['data_set'].columns['_urls'].create()
    pre_meta.tables['tag'].columns['name'].drop()
    post_meta.tables['tag'].columns['_name'].create()
    pre_meta.tables['batch'].columns['description'].drop()
    pre_meta.tables['batch'].columns['name'].drop()
    post_meta.tables['batch'].columns['_arguments'].create()
    post_meta.tables['batch'].columns['_description'].create()
    post_meta.tables['batch'].columns['_disk'].create()
    post_meta.tables['batch'].columns['_flock'].create()
    post_meta.tables['batch'].columns['_glide'].create()
    post_meta.tables['batch'].columns['_job_post'].create()
    post_meta.tables['batch'].columns['_job_pre'].create()
    post_meta.tables['batch'].columns['_kwargs'].create()
    post_meta.tables['batch'].columns['_memory'].create()
    post_meta.tables['batch'].columns['_name'].create()
    post_meta.tables['batch'].columns['_params'].create()
    post_meta.tables['batch'].columns['_params_file'].create()
    post_meta.tables['batch'].columns['_post'].create()
    post_meta.tables['batch'].columns['_pre'].create()
    post_meta.tables['batch'].columns['_share_dir'].create()
    post_meta.tables['batch'].columns['_submit_file'].create()
    post_meta.tables['batch'].columns['_sweep'].create()
    pre_meta.tables['job'].columns['is_completed'].drop()
    pre_meta.tables['job'].columns['process'].drop()
    post_meta.tables['job'].columns['_uid'].create()
    pre_meta.tables['experiment'].columns['description'].drop()
    pre_meta.tables['experiment'].columns['name'].drop()
    post_meta.tables['experiment'].columns['_description'].create()
    post_meta.tables['experiment'].columns['_name'].create()
    pre_meta.tables['user'].columns['password'].drop()
    pre_meta.tables['user'].columns['username'].drop()
    post_meta.tables['user'].columns['_password'].create()
    post_meta.tables['user'].columns['_username'].create()
    pre_meta.tables['result'].columns['blob'].drop()
    post_meta.tables['result'].columns['_blob'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['argument'].create()
    pre_meta.tables['data_collections_tags'].create()
    pre_meta.tables['data_sets_experiments'].create()
    pre_meta.tables['implementations_experiments'].create()
    pre_meta.tables['jobs_tags'].create()
    pre_meta.tables['param'].create()
    pre_meta.tables['users_tags'].create()
    post_meta.tables['collections_tags'].drop()
    pre_meta.tables['data_collection'].columns['description'].create()
    pre_meta.tables['data_collection'].columns['name'].create()
    post_meta.tables['data_collection'].columns['_description'].drop()
    post_meta.tables['data_collection'].columns['_name'].drop()
    pre_meta.tables['algorithm'].columns['description'].create()
    pre_meta.tables['algorithm'].columns['name'].create()
    post_meta.tables['algorithm'].columns['_description'].drop()
    post_meta.tables['algorithm'].columns['_name'].drop()
    pre_meta.tables['implementation'].columns['address'].create()
    pre_meta.tables['implementation'].columns['algorithm_id'].create()
    pre_meta.tables['implementation'].columns['description'].create()
    pre_meta.tables['implementation'].columns['executable'].create()
    pre_meta.tables['implementation'].columns['name'].create()
    post_meta.tables['implementation'].columns['_algorithm_id'].drop()
    post_meta.tables['implementation'].columns['_description'].drop()
    post_meta.tables['implementation'].columns['_executable'].drop()
    post_meta.tables['implementation'].columns['_name'].drop()
    post_meta.tables['implementation'].columns['_setup_scripts'].drop()
    post_meta.tables['implementation'].columns['_urls'].drop()
    pre_meta.tables['data_set'].columns['address'].create()
    pre_meta.tables['data_set'].columns['description'].create()
    pre_meta.tables['data_set'].columns['name'].create()
    post_meta.tables['data_set'].columns['_description'].drop()
    post_meta.tables['data_set'].columns['_name'].drop()
    post_meta.tables['data_set'].columns['_urls'].drop()
    pre_meta.tables['tag'].columns['name'].create()
    post_meta.tables['tag'].columns['_name'].drop()
    pre_meta.tables['batch'].columns['description'].create()
    pre_meta.tables['batch'].columns['name'].create()
    post_meta.tables['batch'].columns['_arguments'].drop()
    post_meta.tables['batch'].columns['_description'].drop()
    post_meta.tables['batch'].columns['_disk'].drop()
    post_meta.tables['batch'].columns['_flock'].drop()
    post_meta.tables['batch'].columns['_glide'].drop()
    post_meta.tables['batch'].columns['_job_post'].drop()
    post_meta.tables['batch'].columns['_job_pre'].drop()
    post_meta.tables['batch'].columns['_kwargs'].drop()
    post_meta.tables['batch'].columns['_memory'].drop()
    post_meta.tables['batch'].columns['_name'].drop()
    post_meta.tables['batch'].columns['_params'].drop()
    post_meta.tables['batch'].columns['_params_file'].drop()
    post_meta.tables['batch'].columns['_post'].drop()
    post_meta.tables['batch'].columns['_pre'].drop()
    post_meta.tables['batch'].columns['_share_dir'].drop()
    post_meta.tables['batch'].columns['_submit_file'].drop()
    post_meta.tables['batch'].columns['_sweep'].drop()
    pre_meta.tables['job'].columns['is_completed'].create()
    pre_meta.tables['job'].columns['process'].create()
    post_meta.tables['job'].columns['_uid'].drop()
    pre_meta.tables['experiment'].columns['description'].create()
    pre_meta.tables['experiment'].columns['name'].create()
    post_meta.tables['experiment'].columns['_description'].drop()
    post_meta.tables['experiment'].columns['_name'].drop()
    pre_meta.tables['user'].columns['password'].create()
    pre_meta.tables['user'].columns['username'].create()
    post_meta.tables['user'].columns['_password'].drop()
    post_meta.tables['user'].columns['_username'].drop()
    pre_meta.tables['result'].columns['blob'].create()
    post_meta.tables['result'].columns['_blob'].drop()
