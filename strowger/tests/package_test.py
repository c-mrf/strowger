import inspect

from strowger import Package
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


class TestGetRoot(PkgMixin, TestCase):
    def prd_none(self, boolean):
        pass

    def dir_exists(self, boolean):
        pass

    def packages(self, boolean):
        pass

    def test_prd_not_none_dir_exists(self):
        pass

    def test_prd_not_none_dir_dne(self):
        pass

    def test_prd_not_none_packages_dir_exists(self):
        pass

    def test_prd_not_none_packages_dir_dne(self):
        pass

    def test_prd_none_envvar_set_attr_unset_dir_exists(self):
        pass
    def test_prd_none_envvar_set_attr_unset_dir_dne(self):
        pass
    def test_prd_none_packages_envvar_set_attr_unset_dir_exists(self):
        pass
    def test_prd_none_packages_envvar_set_attr_unset_dir_dne(self):
        pass

    def test_prd_none_envvar_set_attr_set_matching_dir_exists(self):
        pass
    def test_prd_none_envvar_set_attr_set_matching_dir_dne(self):
        pass
    def test_prd_none_packages_envvar_set_attr_set_matching_dir_exists(self):
        pass
    def test_prd_none_packages_envvar_set_attr_set_matching_dir_dne(self):
        pass

    def test_prd_none_envvar_set_attr_set_unmatching_dir_exists(self):
        pass
    def test_prd_none_envvar_set_attr_set_unmatching_dir_dne(self):
        pass
    def test_prd_none_packages_envvar_set_attr_set_unmatching_dir_exists(self):
        pass
    def test_prd_none_packages_envvar_set_attr_set_unmatching_dir_dne(self):
        pass

    def test_prd_none_envvar_unset_dir_exists(self):
        pass
    def test_prd_none_envvar_unset_dir_dne(self):
        pass
    def test_prd_none_packages_envvar_unset_dir_exists(self):
        pass
    def test_prd_none_packages_envvar_unset_dir_dne(self):
        pass


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
