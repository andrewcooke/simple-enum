from pickle import loads, dumps
from unittest import TestCase
from simplenum import Enum, from_one, bits


class Examples(TestCase):


    def test_colour(self):

        class Colour(Enum):
            red
            green
            blue

        assert isinstance(Colour.red, Colour)
        assert isinstance(Colour.red, tuple)
        assert issubclass(Colour, tuple)
        assert Colour.red.name == Colour.red.value == 'red'
        assert Colour.red == Colour(Colour.red) == Colour('red') == \
               Colour(name='red') == Colour(value='red') == \
               Colour(name='red', value='red')
        assert Colour.red == list(Colour.items())[0]
        assert len(Colour) == 3
        with self.assertRaises(ValueError):
            Colour(value='red', name='blue')
        with self.assertRaises(ValueError):
            Colour(value='pink')
        assert str(Colour.red) == "Colour(name='red', value='red')", str(Colour.red)
        assert repr(Colour.red) == "Colour(name='red', value='red')", repr(Colour.red)
        assert str(list(Colour)) == "['red', 'green', 'blue']", str(list(Colour))
        assert str(list(Colour.items())) == "[Colour(name='red', value='red'), Colour(name='green', value='green'), Colour(name='blue', value='blue')]", str(list(Colour.items()))
        assert str(Colour) == "red, green, blue", str(Colour)
        assert repr(Colour) == "Colour(red: 'red', green: 'green', blue: 'blue')", repr(Colour)

        for (name, value) in Colour.items():
            assert name in Colour
            assert Colour[name] == value
            assert name in set(Colour.keys())
            assert value in set(Colour.values())
        assert Colour.red[0] == 'red'
        assert Colour.red[1] == 'red'


    def test_weekday(self):

        class Weekday(Enum, values=from_one):
            monday, tuesday, wednesday, thursday, friday, saturday, sunday

        assert str(list(Weekday)) == "['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']", str(list(Weekday))
        assert Weekday.monday.value == 1
        assert Weekday['tuesday'] == 2
        assert Weekday.wednesday[1] == 3
        with self.assertRaises(TypeError):
            Weekday['montag'] = 8


    def test_emphasis(self):

        class Emphasis(Enum, values=bits, implicit=False):
            with implicit:
                underline, italic, bold
            bold_italic = italic | bold

        assert Emphasis.bold.value == 4
        assert Emphasis.bold_italic.value == 6


    def test_duplicate(self):

        with self.assertRaises(ValueError):
            class Error(Enum, implicit=False, values=from_one):
                with implicit: one
                another_one = 1

        class MulitlingualWeekday(Enum, implicit=False, values=from_one, allow_aliases=True):
            with implicit:
                monday, tuesday, wednesday, thursday, friday, saturday, sunday
            lunes, martes, miercoles, jueves, viernes, sabado, domingo = \
                monday, tuesday, wednesday, thursday, friday, saturday, sunday

        assert str(MulitlingualWeekday.lunes) == "MulitlingualWeekday(name='monday', value=1)", str(MulitlingualWeekdays.lunes)
        assert str(MulitlingualWeekday('martes')) == "MulitlingualWeekday(name='tuesday', value=2)", str(MulitlingualWeekdays('lunes'))


class Pickle(Enum):
    red, green, blue

class PickleTest(TestCase):

    def test_pickle(self):
        assert Pickle.red is loads(dumps(Pickle.red))
        assert Pickle is loads(dumps(Pickle))


class MethodTest(TestCase):
    '''This isn't a particularly good idea.'''

    def test_methods(self):

        class Animal(Enum, implicit=False):

            @property
            def legs(self):
                return self.value[0]

            @property
            def sound(self):
                return self.value[1]

            def talk(self):
                return self.sound

            def __str__(self):
                return '%s has %d legs and says %s' % \
                       (self.name, self.legs, self.talk())

            pig = 4, 'oink'
            hen = 2, 'cluck'

        assert str(Animal.pig) == "pig has 4 legs and says oink", str(Animal.pig)
