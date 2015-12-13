from os import path
from strowger import Service
from strowger.tests.package_test import PkgMixin
from unittest import TestCase


prd = None

class SvcMixin(object):
    def setUp(self):
        super(SvcMixin, self).setUp()
        service = 'SectionOne'
        shorthand = 'so'
        self.service = Service(service=service, shorthand=shorthand)
        self.uri = 'uri'
        self.assertEqual(self.service.service, service)

class TestPkgConfig(SvcMixin, PkgMixin, TestCase):
    def setUp(self):
        super(TestPkgConfig, self).setUp()
        self.package.root_gvar = 'prd'

    def test_find_test_root(self):
        test_root = self.package.get_root_dir()
        self.assertEqual(test_root, path.dirname(path.abspath(__file__)))

    def test_find_config_successfully(self):
        test_root = self.package.get_root_dir()
        self.service.configs = path.join(test_root, 'config')
        options = self.service._read_config(environment='environment_one')
        self.assertIsNotNone(options)
        self.assertIsInstance(options, dict)
        self.assertEqual(options[self.uri], 'hello://world')

    def test_find_config_unsuccessfully(self):
        test_root = self.package.get_root_dir()
        self.service.configs = path.join(test_root, 'config')
        with self.assertRaises(IOError):
            self.service._read_config(environment='environment_dne')

    def test_read_config_specified_state(self):
        test_root = self.package.get_root_dir()
        self.service.configs = path.join(test_root, 'config')
        options = self.service._read_config(environment='environment_one', state='testing')
        self.assertIsNotNone(options)
        self.assertIsInstance(options, dict)
        self.assertEqual(options[self.uri], 'hello://there')


