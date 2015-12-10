import inspect
from strowger import Package
from unittest import TestCase

Bob = None

class NewPackage(Package):
    def __init__(self, name):
        super(NewPackage, self).__init__(name)

    def stack(self):
        return inspect.stack()

    def currentframe(self):
        return inspect.currentframe()

    def currentframe_num(self, num):
        return inspect.currentframe(num)

    def globalvars(self):
        return inspect.currentframe().f_globals

    def bob(self):
        return inspect.currentframe().f_globals['Bob']

    def setbob(self, name):
        inspect.currentframe().f_globals['Bob'] = name

class TestPackage(TestCase):
    def setUp(self):
        super(TestPackage, self).setUp()
        self.tp = NewPackage('boo')

    def test_currentframe_num(self):
        cf = self.tp.currentframe()
        cf1 = self.tp.currentframe_num(1)
        self.assertEqual(cf.f_globals, cf1.f_globals)

    def test_bob(self):
        self.assertFalse(self.tp.bob())

    def test_set_bob(self):
        self.assertFalse(self.tp.bob())
        cf = self.tp.currentframe()
        self.assertFalse(cf.f_globals['Bob'])

        bname = 'Bobby boy'
        self.tp.setbob(bname)
        self.assertEqual(self.tp.bob(), bname)
        self.assertEqual(self.tp.globalvars()['Bob'], bname)



