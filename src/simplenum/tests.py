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
        with self.assertRaises(ValueError):
            Colour(value='red', name='blue')
        with self.assertRaises(ValueError):
            Colour(value='pink')
        assert str(Colour.red) == "Colour(name='red', value='red')", str(Colour.red)
        assert repr(Colour.red) == "Colour(name='red', value='red')", repr(Colour.red)
        assert str(list(Colour)) == "['red', 'green', 'blue']", str(list(Colour))
        assert str(list(Colour.items())) == "", str(list(Colour.items()))

        for (name, value) in Colour.items():
            assert name in Colour
            assert Colour[name] == value
            assert name in set(Colour.keys())
            assert value in set(Colour.values())


    def test_weekday(self):

        class Weekday(Enum, values=from_one):
            monday, tuesday, wednesday, thursday, friday, saturday, sunday

        assert str(list(Weekday)) == "['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']", str(list(Weekday))
        assert Weekday.monday.value == 1
        assert Weekday['tuesday'] == 2
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

        with self.assertRaises(KeyboardInterrupt):
            class Error(Enum, implicit=False):
                a = 1
                b = 1

        class Ok(Enum, implicit=False, allow_aliases=True):
            a = 1
            b = 1
