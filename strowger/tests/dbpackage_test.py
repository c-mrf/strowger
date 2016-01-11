import os

from sqlalchemy import MetaData
from strowger import DBPackage
from strowger.tests import Base
from unittest import TestCase


db_pkg_root = None
engine = None
metadata = None
session = None

class DbPkgMixin(object):
    def setUp(self):
        pkgnm = 'testdbpkg'
        self.package = DBPackage(pkgnm)
        self.package.root_gvar = 'db_pkg_root'
        self.assertIsNone(self.package.fetch_global_val(self.package.root_gvar))
        self.assertEqual(self.package.name, pkgnm)
        self.package.db.config_folder = os.path.join(self.package.get_root_dir(), 'config')



    def tearDown(self):
        base = self.package.fetch_global_val('Base')
        engine = self.package.fetch_global_val('engine')
        metadata = self.package.fetch_global_val('metadata')
        self.assertIsInstance(metadata, MetaData)
        self.assertEqual(base.metadata, metadata)
        self.assertEqual(base.metadata.bind, engine)

        def cleanUp():
            global db_pkg_root, engine, metadata, session
            db_pkg_root = engine = metadata = session = None
            delattr(self, 'package')

        self.addCleanup(cleanUp)
        self.doCleanups()


class TestDBPackageConnection(DbPkgMixin, TestCase):
    def test_default_env(self):
        self.package.configure(services=True, environment='db_testing')
        self.assertIsNotNone(self.package.fetch_global_val(self.package.root_gvar))

        db_uri = self.package.db.get_uri(environment='db_testing')
        self.assertEqual(db_uri, 'sqlite:///dbtesting.db')

    def test_testing_env(self):
        self.package.configure(services=True, environment='db_testing', state='testing')
        self.assertIsNotNone(self.package.fetch_global_val(self.package.root_gvar))

        db_uri = self.package.db.get_uri(environment='db_testing', state='testing')
        self.assertEqual(db_uri, 'sqlite:///dbtestingtesting.db')
