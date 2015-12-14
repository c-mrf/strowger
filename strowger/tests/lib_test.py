
import functools
import strowger.lib as lib

from unittest import TestCase

class Person(object):
    def __init__(self):
        self.pet = Pet()
        self.residence = Residence()

class Pet(object):
    def __init__(self,name='Fido',species='Dog'):
        self.name = name
        self.species = species

class Residence(object):
    def __init__(self,type='House',sqft=None):
        self.type = type
        self.sqft=sqft


class TestGetSetAttr(TestCase):
    def setUp(self):
        super(TestGetSetAttr, self).setUp()
        self.p=Person()
        
    def test_set_get(self):
        lib.rsetattr(self.p,'pet.name','Sparky')
        self.assertEqual(self.p.pet.name, 'Sparky')
        
        lib.rsetattr(self.p,'residence.type','Apartment')
        self.assertEqual(self.p.residence.type, 'Apartment')
