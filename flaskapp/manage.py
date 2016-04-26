#!/usr/bin/env python

import os
import imp

from migrate.versioning import api
from flask.ext.script import (Manager, Server)
from flask.ext.script.commands import (ShowUrls, Clean)
from flask.ext.login import current_user
from squall import create_app
from squall.models import (db, User, DataSet, Implementation)

# default to dev config because no one should use this in production anyway
env = os.environ.get('SQUALL_ENV', 'dev')
app = create_app('squall.settings.%sConfig' % env.capitalize(), env=env)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@app.context_processor
def inject_user():
    return dict(user=current_user)


@app.context_processor
def urls():

    def code_urls(batch):
        implementation = Implementation.query.filter_by(
            id=batch.implementation_id).first()
        return implementation.urls

    def executable(batch):
        implementation = Implementation.query.filter_by(
            id=batch.implementation_id).first()
        return implementation.executable

    def setup_scripts(batch):
        implementation = Implementation.query.filter_by(
            id=batch.implementation_id).first()
        return implementation.setup_scripts

    def data_urls(batch):
        data_set = DataSet.query.filter_by(id=batch.data_set_id).first()
        return data_set.urls

    return dict(code_urls=code_urls,
                executable=executable,
                setup_scripts=setup_scripts,
                data_urls=data_urls)


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """
    return dict(app=app, db=db, User=User)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        the SQLAlchemy models. Creates and initializes an
        SQLAlchemy-migrate repository if none exists.
    """

    # Create New DB Reflecting SQLAlchemy Data Models
    db.create_all(app=app)
    admin = User('admin', '/home/admin', 'password')
    db.session.add(admin)
    db.session.commit()

    # Create SQLAlchemy-migrate Versioning Repository If Absent
    if not os.path.exists(app.config['SQLALCHEMY_MIGRATE_REPO']):
        api.create(app.config['SQLALCHEMY_MIGRATE_REPO'],
                   'database repository')
        api.version_control(app.config['SQLALCHEMY_DATABASE_URI'],
                            app.config['SQLALCHEMY_MIGRATE_REPO'])
        print "SQLAlchemy-migrate Versioning Repository Created in: " +\
            app.config['SQLALCHEMY_MIGRATE_REPO']
    else:
        api.version_control(app.config['SQLALCHEMY_DATABASE_URI'],
                            app.config['SQLALCHEMY_MIGRATE_REPO'],
                            api.version(
                                app.config['SQLALCHEMY_MIGRATE_REPO']))
    print "Database created in: " + app.config['SQLALCHEMY_DATABASE_URI']


@manager.command
def migratedb():
    """ Updates the database and SQLAlchemy-migrate repository
        to a new version containing all of the tables defined
        in the SQLAlchemy data models.
    """

    # Obtain Current Verison
    ver = api.db_version(app.config['SQLALCHEMY_DATABASE_URI'],
                         app.config['SQLALCHEMY_MIGRATE_REPO'])

    # Create Migration Script To Apply Model Changes
    mgr = app.config['SQLALCHEMY_MIGRATE_REPO'] +\
        ('/versions/%03d_migration.py' % (ver+1))
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(app.config['SQLALCHEMY_DATABASE_URI'],
                                 app.config['SQLALCHEMY_MIGRATE_REPO'])
    exec(old_model, tmp_module.__dict__)
    script = api.make_update_script_for_model(
        app.config['SQLALCHEMY_DATABASE_URI'],
        app.config['SQLALCHEMY_MIGRATE_REPO'],
        tmp_module.meta, db.metadata)
    open(mgr, "wt").write(script)

    # Update Database With Migration Script
    api.upgrade(app.config['SQLALCHEMY_DATABASE_URI'],
                app.config['SQLALCHEMY_MIGRATE_REPO'])

    # Obtain & Display Current Version & Migration
    ver = api.db_version(app.config['SQLALCHEMY_DATABASE_URI'],
                         app.config['SQLALCHEMY_MIGRATE_REPO'])
    print('New migration saved as: ' + mgr)
    print('Current databse version: ' + str(ver))


@manager.command
def upgradedb():
    """ Upgradess the database from the current version to the
        latest revision by applying all relevant migrate scripts
        in the SQLAlchemy-migration repository.
    """

    # Update Database To Most Current Revision
    api.upgrade(app.config['SQLALCHEMY_DATABASE_URI'],
                app.config['SQLALCHEMY_MIGRATE_REPO'])

    # Obtain & Display Current Version
    ver = api.db_version(app.config['SQLALCHEMY_DATABASE_URI'],
                         app.config['SQLALCHEMY_MIGRATE_REPO'])
    print("Current database version: " + str(ver))


@manager.command
def downgradedb():
    """ Downgrades the database from the current to the previous
        version contained in the SQLAlchemy-migrate repository.
    """

    # Obtain Current Version
    ver = api.db_version(app.config['SQLALCHEMY_DATABASE_URI'],
                         app.config['SQLALCHEMY_MIGRATE_REPO'])

    # Downgrade Database To Previous Revision
    api.downgrade(app.config['SQLALCHEMY_DATABASE_URI'],
                  app.config['SQLALCHEMY_MIGRATE_REPO'], ver-1)

    # Obtain & Display Current Version
    ver = api.db_version(app.config['SQLALCHEMY_DATABASE_URI'],
                         app.config['SQLALCHEMY_MIGRATE_REPO'])
    print("Current database version: " + str(ver))


if __name__ == "__main__":
    manager.run()
