from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
algorithms_experiments = Table('algorithms_experiments', pre_meta,
    Column('experiment_id', INTEGER),
    Column('algorithm_id', INTEGER),
)

collections_experiments = Table('collections_experiments', pre_meta,
    Column('experiment_id', INTEGER),
    Column('collection_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['algorithms_experiments'].drop()
    pre_meta.tables['collections_experiments'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['algorithms_experiments'].create()
    pre_meta.tables['collections_experiments'].create()
