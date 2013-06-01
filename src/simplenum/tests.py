from collections import namedtuple
from unittest import TestCase
from simplenum import Enum


class Examples(TestCase):

    def test_colour(self):

        class Colour(Enum):
            red
            green
            blue

        assert Colour.red == 'red'


foo = namedtuple('foo', 'name value')
