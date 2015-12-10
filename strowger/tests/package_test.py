from strowger import Package
from unittest import TestCase

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


class TestGetRoot(PkgMixin):
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


class TestGlobalVars(PkgMixin):
    def test_fetch_val_for_gvar_exists(self):
        pass
    def test_fetch_val_for_gvar_dne(self):
        pass
    def test_update_gvar_exists(self):
        pass
    def test_update_gvar_dne(self):
        pass
