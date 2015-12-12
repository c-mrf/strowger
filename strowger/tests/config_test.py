from strowger.tests.config_test import PkgMixin
from unittest import TestCase

class TestPkgConfig(PkgMixin, TestCase):
    def test_find_config_successfully(self):
        pass

    def test_find_config_unsuccessfully(self):
        pass

    def test_read_config_correctly(self):
        pass

    def read_config_with_deafult_state(self):
        pass

    def read_config_default_incorrect_state(self):
        pass

    def read_config_specified_state(self):
        pass


class TestDBPackage(PkgMixin, TestCase):
    pass
