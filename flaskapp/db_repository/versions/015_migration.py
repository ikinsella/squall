from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
algorithms_experiments = Table('algorithms_experiments', post_meta,
    Column('experiment_id', Integer),
    Column('algorithm_id', Integer),
)

collections_experiments = Table('collections_experiments', post_meta,
    Column('experiment_id', Integer),
    Column('collection_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['algorithms_experiments'].create()
    post_meta.tables['collections_experiments'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['algorithms_experiments'].drop()
    post_meta.tables['collections_experiments'].drop()
