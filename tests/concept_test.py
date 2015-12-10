import inspect
from strowger import Package

Bob = None

class TestPackage(Package):
    def __init__(self, name):
        super(TestPackage, self).__init__(name)

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


tp = TestPackage('boo')

s = tp.stack()
cf = tp.currentframe()
gv = tp.globalvars()
b = tp.bob()



