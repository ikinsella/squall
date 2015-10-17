#! ../env/bin/python
# -*- coding: utf-8 -*-
from appname import create_app
import os

basedir = os.path.abspath(os.path.dirname(__name__))


class TestConfig:
    def test_dev_config(self):
        """ Tests if the development config loads correctly """

        app = create_app('appname.settings.DevConfig', env='dev')

        assert app.config['DEBUG'] is True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == \
            'sqlite:///' + os.path.join(basedir, 'database.db')
        assert app.config['CACHE_TYPE'] == 'null'

    def test_test_config(self):
        """ Tests if the test config loads correctly """

        app = create_app('appname.settings.TestConfig', env='dev')

        assert app.config['DEBUG'] is True
        assert app.config['SQLALCHEMY_ECHO'] is True
        assert app.config['CACHE_TYPE'] == 'null'

    def test_prod_config(self):
        """ Tests if the production config loads correctly """

        app = create_app('appname.settings.ProdConfig', env='prod')

        assert app.config['SQLALCHEMY_DATABASE_URI'] == \
            'sqlite:///' + os.path.join(basedir, 'database.db')
        assert app.config['CACHE_TYPE'] == 'simple'
