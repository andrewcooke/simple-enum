
from collections import OrderedDict, namedtuple
from itertools import count
from types import MappingProxyType


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

def dunder(name):
    return name[:2] == name[-2:] == '__'


class ClassDict(OrderedDict):

    def __init__(self, implicit=False, values=names):
        super().__init__()
        self.implicit = implicit
        self.values = values

    def __enter__(self):
        self.implicit = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.implicit = False

    def __getitem__(self, name):
        if name not in self:
            if self.implicit and Enum and not dunder(name):
                super().__setitem__(name, self.values(name))
            elif name == 'implicit':
                return self
        return super().__getitem__(name)

    def __setitem__(self, name, value):
        if self.implicit and Enum and not dunder(name):
            raise TypeError('Cannot use explicit value for %s' % name)
        return super().__setitem__(name, value)

    def split(self):
        enums, others = OrderedDict(), dict()
        for name in self:
            if dunder(name):
                others[name] = self[name]
            else:
                enums[name] = self[name]
        return enums, others


class EnumMeta(type):

    def __init__(metacls, cls, bases, dict, **kargs):
        super().__init__(cls, bases, dict)

    @classmethod
    def __prepare__(metacls, name, bases, implicit=True, values=names, **kargs):
        return ClassDict(implicit=implicit, values=values())

    def __new__(metacls, name, bases, prepared, allow_aliases=False, **kargs):
        enums, others = prepared.split()
        cls = super().__new__(metacls, name, bases, others)
        cls._enums_by_name, cls._enums_by_value = {}, OrderedDict()
        for name in enums:
            value = enums[name]
            enum = cls.__new__(cls, name, value)
            if value in cls._enums_by_value:
                if allow_aliases:
                    cls._enums_by_name[name] = cls._enums_by_value[value]
                else:
                    raise ValueError('Duplicate value (%r) for %s and %s' %
                                     (value, cls._enums_by_value[value].name, name))
            else:
                cls._enums_by_value[value] = enum
                cls._enums_by_name[name] = enum
        cls._enums = MappingProxyType(
                        OrderedDict((enum.name, enum.value)
                                    for enum in cls._enums_by_value.values()))
        return cls

    def __contains__(cls, name): return cls._enums.__contains__(name)
    def __iter__(cls): return cls._enums.__iter__()
    def __getitem__(cls, name): return cls._enums.__getitem__(name)
    def keys(cls): return cls._enums.keys()
    def values(cls): return cls._enums.values()

    def items(cls):
        return iter(cls._enums_by_value[value] for value in cls._enums_by_value)

    def __getattr__(cls, name):
        try:
            return cls._enums_by_name[name]
        except KeyError:
            raise AttributeError(name)

    def __call__(cls, name=None, value=None):
        if type(name) is cls:
            if value is None or value == name.value:
                return name
        elif value is None:
            if name is None:
                raise ValueError('Give name or value')
            elif name in cls._enums_by_name:
                return cls._enums_by_name[name]
            else:
                raise ValueError('No name %r' % name)
        elif name is None:
            if value in cls._enums_by_value:
                return cls._enums_by_value[value]
            else:
                raise ValueError('No value %r' % value)
        elif name in cls._enums_by_name:
            enum = cls._enums_by_name[name]
            if value in cls._enums_by_value and \
                        enum is cls._enums_by_value[value]:
                return enum
        raise ValueError('Inconsistent name (%r) and value (%r)' %
                        (name, value))


class Enum(namedtuple('Enum', 'name, value'), metaclass=EnumMeta):

    def __new__(cls, *args, **kwargs):
        # this is called on creation and by pickle.  we try __call__ first
        # so that unpickling retrieves an existing instance.  if that fails
        # then we create a new instance.
        try:
            return cls.__call__(*args, **kwargs)
        except ValueError:
            return super().__new__(cls, *args, **kwargs)
