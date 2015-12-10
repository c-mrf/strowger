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
    pass
