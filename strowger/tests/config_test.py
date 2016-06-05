from os import path
from strowger import Service
from strowger.tests.package_test import PkgMixin
from unittest import TestCase


prd = None
svc_global = None
service = 'SectionOne'
shorthand = 'so'

test_svc_config = "svc_config"

class SvcMixin(object):
    def setUp(self):
        super(SvcMixin, self).setUp()
        globalvars = {'globalvar': 'svc_global'}
        self.service = Service(service=service, shorthand=shorthand, globalvars=globalvars)
        self.uri = self.service.uri = 'uri'
        self.assertEqual(self.service.service, service)

class TestPkgConfig(SvcMixin, PkgMixin, TestCase):
    def setUp(self):
        super(TestPkgConfig, self).setUp()
        self.package.root_gvar = 'prd'

        test_root = self.package.get_root_dir()
        self.service.config_folder = path.join(test_root, 'config')

    def tearDown(self):
        if test_svc_config in globals():
            del globals()[test_svc_config]

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
        options = self.service._read_config(environment='environment_one', state='testing')
        self.assertIsNotNone(options)
        self.assertIsInstance(options, dict)
        self.assertEqual(options[self.uri], 'hello://there')

    def test_configure_service_via_package(self):
        @self.service.configure_func
        def configure_tstpkg_service(environment=None, state=None, **kwargs):
            opts = self.service._read_config(environment=environment, state=state)
            self.assertEqual(opts[self.uri], self.service.get_uri(environment=environment, state=state))

        self.package.add_service(self.service)
        self.package.configure(pkg_root=False, services=True, environment='environment_one')

    def test_configure_service_via_package_vars_in_str(self):
        @self.service.configure_func
        def configure_tstpkg_service(environment=None, state=None, **kwargs):
            opts = self.service._read_config(environment=environment, state=state)
            self.assertEqual(opts[self.uri], self.service.get_uri(environment=environment, state=state))

        self.package.add_service(self.service)
        self.package.configure(pkg_root=False, services=True, environment='environment_three', state='testing')

    def test_configure_service_manually_via_package(self):
        @self.service.configure_func
        def configure_tstpkg_service(environment=None, state=None, **kwargs):
            opts = self.service._read_config(environment=environment, state=state)
            self.assertEqual(opts[self.uri], self.service.get_uri(environment=environment, state=state))
            self.package.update_global_var(test_svc_config, True)

        self.package.add_service(self.service)
        self.package.configure(pkg_root=False, services=[shorthand], environment='environment_one')
        self.assertEquals(True, self.package.fetch_global_val(test_svc_config))
        
    def test_configure_service_manually_via_package_fake_service(self):
        @self.service.configure_func
        def configure_tstpkg_service(environment=None, state=None, **kwargs):
            opts = self.service._read_config(environment=environment, state=state)
            self.assertEqual(opts[self.uri], self.service.get_uri(environment=environment, state=state))
            self.package.update_global_var(test_svc_config, True)

        self.package.add_service(self.service)
        self.package.configure(pkg_root=False, services=['fake'], environment='environment_one')

        with self.assertRaises(ValueError):
            self.package.fetch_global_val(test_svc_config)
