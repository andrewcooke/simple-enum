
from collections import OrderedDict
from itertools import count
from operator import itemgetter


def names():
    def value(name):
        return name
    return value

def from_counter(start, step=1):
    def outer():
        counter = count(start, step)
        def value(name):
            nonlocal counter
            return next(counter)
        return value
    return outer

from_one = from_counter(1)
from_zero = from_counter(0)

def bits():
    count = 0
    def value(name):
        nonlocal count
        count += 1
        return 2 ** (count - 1)
    return value


Enum = None
SPECIAL_FIELDS = {'__module__', '__qualname__'}

class ClassDict(OrderedDict):
    '''
    The dictionary supplied by EnumMeta to store the class contents.  We
    provide a default value when implicit is true, and allow implicit to
    be enabled via "with implicit".

    An ordered dict is needed to preserve the order of side-effects (things
    like which alias is preferred).
    '''

    def __init__(self, implicit=False, values=names):
        super().__init__()
        self.implicit = implicit
        self.values = values

    def __enter__(self):
        self.implicit = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.implicit = False

    def __getitem__(self, item):
        if self.implicit and Enum:
            if item not in self:
                super().__setitem__(item, self.values(item))
        else:
            if item not in self and item == 'implicit':
                return self
        return super().__getitem__(item)

    def __setitem__(self, name, value):
        if self.implicit and Enum and name not in SPECIAL_FIELDS:
            raise TypeError('Cannot use explicit value for %s' % name)
        return super().__setitem__(name, value)


class EnumMeta(type):

    @classmethod
    def __prepare__(metacls, name, bases,
                    implicit=True, values=names, allow_aliases=False):
        return ClassDict(implicit=implicit, values=values())


class Enum(tuple, metaclass=EnumMeta):

    __slots__ = ()

    name = property(itemgetter(0), doc='Enum name')
    value = property(itemgetter(1), doc='Enum value')
