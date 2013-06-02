
from collections import OrderedDict, namedtuple
from itertools import count
from types import MappingProxyType


'''
A simpler Enum for Python 3.

(c) 2013 Andrew Cooke, andrew@acooke.org;
released into the public domain for any use, but with absolutely no warranty.
'''


def names():
    '''Provide a value for each enum which is the name itself.'''
    def value(name):
        return name
    return value

def from_counter(start, step=1):
    '''Provide a value for each enum from a counter.'''
    def outer():
        counter = count(start, step)
        def value(name):
            nonlocal counter
            return next(counter)
        return value
    return outer

from_one = from_counter(1)
from_one.__doc__ = 'Provide a value for each enum that counts from one.'
from_one.__name__ = 'from_one'

from_zero = from_counter(0)
from_zero.__doc__ = 'Provide a value for each enum that counts from zero.'
from_zero.__name__ = 'from_zero'

def bits():
    '''Provide a value for each enum that is a distinct bit (1, 2, 4, etc).'''
    count = 0
    def value(name):
        nonlocal count
        count += 1
        return 2 ** (count - 1)
    return value

# Used to detect EnumMeta creation in the dict.  If Enum is false then we
# disable implicit values.
Enum = None

def dunder(name):
    '''Test for special names.'''
    return name[:2] == name[-2:] == '__'


class ClassDict(OrderedDict):
    '''
    This is the dictionary used while creating Enum instances.  It provides
    default values when `implicit` is true.  This can either be enabled by
    default, or within a `with` context.
    '''

    def __init__(self, implicit=False, values=names):
        '''Setting `implicit` will provide default values from `values`.'''
        super().__init__()
        self.implicit = implicit
        self.values = values()

    def __enter__(self):
        '''Enable implicit values within a `with` context.'''
        self.implicit = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Disable implicit values on leaving a `with` context.'''
        self.implicit = False

    def __getitem__(self, name):
        '''Provide an item from the dictionary.  Values are created if
        `implicit` is currently true.'''
        if name not in self:
            if self.implicit and Enum and not dunder(name):
                super().__setitem__(name, self.values(name))
            elif name == 'implicit':
                return self
        return super().__getitem__(name)

    def __setitem__(self, name, value):
        '''Set a value in the dictionary.  Setting is disabled for user
        values (not dunders) if `implicit` is true.  This helps avoid
        confusion from expressions involving shadowed global names.'''
        if self.implicit and Enum and not dunder(name):
            raise TypeError('Cannot use explicit value for %s' % name)
        return super().__setitem__(name, value)

    def split(self):
        '''Separate the enums from the special values (dunders and
        descriptors; we assume the latter are methods).'''
        enums, others = OrderedDict(), dict()
        for name in self:
            value = self[name]
            if dunder(name) or hasattr(value, '__get__'):
                others[name] = value
            else:
                enums[name] = value
        return enums, others


class EnumMeta(type):
    '''
    This does three main things: (1) it manages the construction of both
    the Enum class and its sub-classes via `__prepare__` and `__new__`;
    (2) it delegates the `dict` API to the `cls._enums` member so that
    classes look like dictionaries; (3) it provides retrieval of named tuples
    via `__call__`.
    '''

    def __init__(metacls, cls, bases, dict, **kargs):
        '''Called during class construction.  Drop kargs.'''
        super().__init__(cls, bases, dict)

    @classmethod
    def __prepare__(metacls, name, bases, implicit=True, values=names, **kargs):
        '''Provide the class dictionary (which provides implicit values).'''
        return ClassDict(implicit=implicit, values=values)

    def __new__(metacls, name, bases, prepared, allow_aliases=False, **kargs):
        '''Create the class and then the named tuples, saving the latter in
        the former.'''
        enums, others = prepared.split()
        cls = super().__new__(metacls, name, bases, others)
        cls._enums_by_name, cls._enums_by_value = {}, OrderedDict()
        for name in enums:
            value = enums[name]
            enum = cls.__new__(cls, name, value)
            # handle aliases
            if value in cls._enums_by_value:
                if allow_aliases:
                    cls._enums_by_name[name] = cls._enums_by_value[value]
                else:
                    raise ValueError('Duplicate value (%r) for %s and %s' %
                                     (value, cls._enums_by_value[value].name, name))
            else:
                cls._enums_by_value[value] = enum
                cls._enums_by_name[name] = enum
        # build the delegate from values as that does not include aliases
        cls._enums = MappingProxyType(
                        OrderedDict((enum.name, enum.value)
                                    for enum in cls._enums_by_value.values()))
        return cls

    # Delegate dictionary methods.
    def __contains__(cls, name): return cls._enums.__contains__(name)
    def __iter__(cls): return cls._enums.__iter__()
    def __getitem__(cls, name): return cls._enums.__getitem__(name)
    def keys(cls): return cls._enums.keys()
    def values(cls): return cls._enums.values()

    def items(cls):
        '''This can be seen in two ways.  As a dictionary method it returns
        `(name, value)` pairs.  But it also returns a list of named tuples
        that are the enumerations themselves.'''
        return iter(cls._enums_by_value[value] for value in cls._enums_by_value)

    def __getattr__(cls, name):
        '''Provide access to named tuples.'''
        try: return cls._enums_by_name[name]
        except KeyError: raise AttributeError(name)

    def __call__(cls, name=None, value=None):
        '''Retrieve named tuples by name or value.  We also special case
        calling with an existing instance.'''
        if type(name) is cls:
            if value is None or value == name.value: return name
        elif value is None:
            if name is None: raise ValueError('Give name or value')
            if name in cls._enums_by_name: return cls._enums_by_name[name]
            raise ValueError('No name %r' % name)
        elif name is None:
            if value in cls._enums_by_value: return cls._enums_by_value[value]
            raise ValueError('No value %r' % value)
        elif name in cls._enums_by_name:
            enum = cls._enums_by_name[name]
            if value in cls._enums_by_value and \
                        enum is cls._enums_by_value[value]: return enum
        raise ValueError('Inconsistent name (%r) and value (%r)' %
                        (name, value))


class Enum(namedtuple('Enum', 'name, value'), metaclass=EnumMeta):
    '''
    The super class for enumerations.  The body of sub-classes should
    typically contain a list of enumeration names.
    '''

    def __new__(cls, *args, **kwargs):
        '''Called on instance creation and by pickle.  We try __call__ first
        so that unpickling retrieves an existing instance.  If that fails
        then we create a new instance.'''
        try: return cls.__call__(*args, **kwargs)
        except ValueError: return super().__new__(cls, *args, **kwargs)

    def _make(self): raise TypeError('Enum contents cannot be extended')
