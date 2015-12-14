import os

from sqlalchemy import MetaData
from strowger import DBPackage, Package
from strowger.tests import Base
from unittest import TestCase

package_root = None
test_gvar = 'hello_test_gvar'

class PkgMixin(object):
    def setUp(self):
        super(PkgMixin, self).setUp()
        pkgnm = 'testpkg'
        self.package = Package(pkgnm)
        self.assertEqual(self.package.name, pkgnm)


class TestSetRoot(PkgMixin, TestCase):
    def test_successful_setting(self):
        package_root_var = 'TSTPKG_ROOT'
        self.package.set_root_var(package_root_var)
        self.assertEqual(self.package.root_envvar, package_root_var)

    def test_fail_on_reassign_root_envvar(self):
        self.package.set_root_var('test')
        with self.assertRaises(AssertionError):
            self.package.set_root_var('test2')

        self.assertEqual(self.package.root_envvar, 'test')

prdpkg = None
prd_not_none = os.path.dirname(os.path.abspath(__file__))
prd_not_none_dne = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dne_dir')

packages = ('testpkg', 'pkgdir')
packages_dne = ('testpkg', 'pkdgirdne')

class TestGetRoot(PkgMixin, TestCase):
    dir_exists = None
    prd_none = None
    envvar = None
    packages = None

    def tearDown(self):
        try:
            os.unsetenv('%s_ROOT' % self.package.name.upper())
        except KeyError:
            pass
        if self.package.root_envvar:
            try:
                os.unsetenv(self.package.root_envvar)
            except KeyError:
                pass
        super(TestGetRoot, self).tearDown()

    def dir_exists(self, boolean):
        self.dir_exists = boolean

    def prd_none(self, boolean):
        self.prd_none = boolean
        if self.prd_none:
            self.package.root_gvar = 'prdpkg'
            x = self.package.fetch_global_val(self.package.root_gvar)
            self.assertEqual(x, None)
        else:
            if self.dir_exists:
                self.package.root_gvar = 'prd_not_none'
            else:
                self.package.root_gvar = 'prd_not_none_dne'
            assert self.package.fetch_global_val(self.package.root_gvar) is not None

    def packages(self, boolean):
        if boolean:
            if self.dir_exists:
                self.packages = packages
            else:
                self.packages = packages_dne
            assert self.packages is not None
        else:
            self.packages = None
            assert self.packages is None

    def envvar_set(self, boolean, dne=False):
        self.envvar = boolean
        if boolean:
            if self.dir_exists and not dne:
                os.environ[self.package.get_root_var()] = self.package.fetch_global_val('prd_not_none')
            else:
                os.environ[self.package.get_root_var()] = self.package.fetch_global_val('prd_not_none_dne')

    def verify_root(self, root_dir=None):
        if root_dir:
            test_dir = self.package.get_root_dir()
            self.assertEqual(test_dir, root_dir)
        else:
            if self.dir_exists:
                if self.packages:
                    correct = os.path.join(self.package.fetch_global_val('prd_not_none'), *self.packages)
                else:
                    correct = self.package.fetch_global_val('prd_not_none')
                test_dir = self.package.get_root_dir(packages=self.packages)
                self.assertEqual(test_dir, correct)
                if self.envvar:
                    assert os.environ[self.package.get_root_var()] is not None
                #print "\n\t %s" % correct
            else:
                with self.assertRaises(ValueError):
                    self.package.get_root_dir(packages=self.packages)

    """
    Group 1
    """
    def test_prd_not_none_dir_exists(self):
        self.dir_exists(True)
        self.packages(False)
        self.prd_none(False)
        self.envvar_set(True, dne=True)
        self.verify_root()

    def test_prd_not_none_dir_dne(self):
        self.dir_exists(False)
        self.packages(False)
        self.prd_none(False)
        self.envvar_set(True, dne=True)
        self.verify_root()

    def test_prd_not_none_packages_dir_exists(self):
        self.dir_exists(True)
        self.packages(True)
        self.prd_none(False)
        self.envvar_set(True, dne=True)
        self.verify_root()

    def test_prd_not_none_packages_dir_dne(self):
        self.dir_exists(False)
        self.packages(True)
        self.prd_none(False)
        self.envvar_set(True, dne=True)
        self.verify_root()

    """
    Group 2
    """
    def test_prd_none_envvar_set_attr_unset_dir_exists(self):
        self.dir_exists(True)
        self.packages(False)
        self.prd_none(True)
        self.envvar_set(True)
        self.verify_root()

    def test_prd_none_envvar_set_attr_unset_dir_dne(self):
        self.dir_exists(False)
        self.packages(False)
        self.prd_none(True)
        self.envvar_set(True)
        self.verify_root()

    def test_prd_none_packages_envvar_set_attr_unset_dir_exists(self):
        self.dir_exists(True)
        self.packages(True)
        self.prd_none(True)
        self.envvar_set(True)
        self.verify_root()

    def test_prd_none_packages_envvar_set_attr_unset_dir_dne(self):
        self.dir_exists(False)
        self.packages(True)
        self.prd_none(True)
        self.envvar_set(True)
        self.verify_root()


    """
    Group 3
    """
    def test_prd_none_envvar_set_attr_set_matching_dir_exists(self):
        self.dir_exists(True)
        self.packages(False)
        self.prd_none(True)
        default_envvar = self.package.get_root_var()
        os.environ[default_envvar] = self.package.fetch_global_val("prd_not_none_dne")
        self.package.root_envvar = 'ANOTHER_ROOTVAR'
        self.envvar_set(True)
        self.verify_root()

    def test_prd_none_envvar_set_attr_set_matching_dir_dne(self):
        self.dir_exists(False)
        self.packages(False)
        self.prd_none(True)
        default_envvar = self.package.get_root_var()
        os.environ[default_envvar] = self.package.fetch_global_val("prd_not_none_dne")
        self.package.root_envvar = 'ANOTHER_ROOTVAR'
        self.envvar_set(True, dne=True)
        self.verify_root()

    def test_prd_none_packages_envvar_set_attr_set_matching_dir_exists(self):
        self.dir_exists(True)
        self.packages(True)
        self.prd_none(True)
        default_envvar = self.package.get_root_var()
        os.environ[default_envvar] = self.package.fetch_global_val("prd_not_none_dne")
        self.package.root_envvar = 'ANOTHER_ROOTVAR'
        self.envvar_set(True)
        self.verify_root()

    def test_prd_none_packages_envvar_set_attr_set_matching_dir_dne(self):
        self.dir_exists(False)
        self.packages(True)
        self.prd_none(True)
        default_envvar = self.package.get_root_var()
        os.environ[default_envvar] = self.package.fetch_global_val("prd_not_none_dne")
        self.package.root_envvar = 'ANOTHER_ROOTVAR'
        self.envvar_set(True, dne=True)
        self.verify_root()


    """
    Group 4
    """
    def test_prd_none_envvar_set_attr_set_unmatching_dir_exists(self):
        self.dir_exists(True)
        self.packages(False)
        self.prd_none(True)
        default_envvar = self.package.get_root_var()
        os.environ[default_envvar] = self.package.fetch_global_val("prd_not_none_dne")
        self.package.root_envvar = 'ANOTHER_ROOTVAR'
        self.envvar_set(False)
        self.verify_root()

    def test_prd_none_packages_envvar_set_attr_set_unmatching_dir_exists(self):
        self.dir_exists(True)
        self.packages(True)
        self.prd_none(True)
        default_envvar = self.package.get_root_var()
        os.environ[default_envvar] = self.package.fetch_global_val("prd_not_none")
        self.package.root_envvar = 'ANOTHER_ROOTVAR'
        self.envvar_set(False)
        self.verify_root()


    """
    Group 5
    """
    def test_prd_none_envvar_unset_dir_exists(self):
        self.dir_exists(True)
        self.packages(False)
        self.prd_none(True)
        self.envvar_set(False)
        self.verify_root()

    def test_prd_none_packages_envvar_unset_dir_exists(self):
        self.dir_exists(True)
        self.packages(True)
        self.prd_none(True)
        self.envvar_set(False)
        self.verify_root()

    def test_prd_none_packages_envvar_unset_dir_dne(self):
        self.dir_exists(False)
        self.packages(True)
        self.prd_none(True)
        self.envvar_set(False)
        self.verify_root()


class TestGlobalVars(PkgMixin, TestCase):
    gvar_dne = 'test_gvar_dne'
    gvar = 'test_gvar'
    new_val = 'new_hello'

    def test_fetch_val_gvar_exists(self):
        global test_gvar
        self.assertEqual(test_gvar, self.package.fetch_global_val(self.gvar))

    def test_fetch_val_gvar_dne(self):
        with self.assertRaises(ValueError):
            self.package.fetch_global_val(self.gvar_dne)

    def test_update_gvar_exists(self):
        self.package.update_global_var(self.gvar, self.new_val)
        self.assertEqual(self.new_val, self.package.fetch_global_val(self.gvar))
        self.test_fetch_val_gvar_exists()

    def test_update_gvar_dne(self):
        self.package.update_global_var(self.gvar_dne, self.new_val)
        self.assertEqual(self.new_val, self.package.fetch_global_val(self.gvar_dne))

db_pkg_root = None
engine = None
metadata = None
session = None

class SvcMixin(object):
    def setUp(self):
        def cleanUp():
            global db_pkg_root, engine, metadata, session
            db_pkg_root = engine = metadata = session = None
            delattr(self, 'package')

        self.addCleanup(cleanUp)

        super(SvcMixin, self).setUp()
        pkgnm = 'testpkg'
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

        self.doCleanups()


class TestDBPackage(SvcMixin, TestCase):
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
