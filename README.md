simple-enum
===========

A simpler Enum for Python 3.

* [Getting Started](#getting-started)
  * [The Dictionary Point Of View](#the-dictionary-point-of-view)
  * [The Named Tuple Point Of View](#the-named-tuple-point-of-view)
  * [That's It, Really](#thats-it-really)
* [Advanced Use](#advanced-use)
  * [Retrieving Tuples](#retrieving-tuples)
  * [Providing Implicit Values](#providing-implicit-values)
  * [Providing Explicit Values](#providing-explicit-values)
  * [Aliases](#aliases)
* [Discussion](#discussion)
  * [Background](#background)
  * [Differences With Enum](#differences-with-enum)
  * [The Danger Of Magic](#the-danger-of-magic)
  * [Technical Details](#technical-details)
  * [TYCDWTSE (TYCDWTSE)](#things-you-can-do-with-the-simpler-enum-that-you-cant-do-with-the-standard-enum)
  * [Credits](#credits)
* [Legalities](#legalities)

Getting Started
---------------

Install `simple-enum` from
[PyPI](https://pypi.python.org/pypi/simple-enum):

```sh
easy_install simple-enum
```

### The Dictionary Point Of View

An Enum is an ordered, immutable dictionary.  You only need to provide the
names:

```python
>>> from simplenum import Enum
>>> class Colour(Enum):
...     red
...     green
...     blue
...
>>> list(Colour)
['red', 'green', 'blue']
>>> 'red' in Colour
True
```

By default, the dictionary values are the names themselves:

```python
>>> Colour['red']
'red'
```

but you can change that using `values`:

```python
>>> from simplenum import from_one
>>> class Weekday(Enum, values=from_one):
...     monday, tuesday, wednesday, thursday, friday, saturday, sunday
...
>>> Weekday['monday']
1
```

### The Named Tuple Point Of View

An Enum is *also* an ordered, immutable set of named tuples:

```python
>>> class Colour(Enum):
...     red
...     green
...     blue
...
>>> Colour.red
Colour(name='red', value='red')
>>> Colour.red.name
'red'
>>> Colour.red[1]
'red'
>>> list(Colour.items())
[Colour(name='red', value='red'), Colour(name='green', value='green'), Colour(name='blue', value='blue')]
>>> isinstance(Colour.red, Colour)
True
```

As before, you can specify the `values`:

```python
>>> class Weekday(Enum, values=from_one):
...     monday, tuesday, wednesday, thursday, friday, saturday, sunday
...
>>> Weekday.monday.value
1
>>> Weekday.tuesday
Weekday(name='tuesday', value=2)
```

### That's It, Really

The two points of view are consistent - you can mix and match as you please.

OK, so there is a little more below.  But in most cases the above should be
all you need.

Advanced Use
------------

### Retrieving Tuples

If you have a name, or value, you can get the tuple by calling the class:

```python
>>> Weekday('wednesday')
Weekday(name='wednesday', value=3)
>>> Weekday(value=4).name
thursday
```

### Providing Implicit Values

The `values` parameter expects a no-argument function (called once per class
definition), which returns a second function from names to values.

So, for example, to give random values:

```python
>>> from random import random
>>> def random_values():
...     def value(name):
...         return random()
...     return value
...
>>> class Random(Enum, values=random_values):
...     a, b, c
...
>>> list(Random.items())
[Random(name='a', value=0.49267653329514594), Random(name='b', value=0.5521902021074088), Random(name='c', value=0.5540234367417308)]
```

### Providing Explicit Values

If you want to specify the values explicitly, use `implicit=False`:

```python
>>> class Favourite(Enum, implicit=False):
...     food = 'bacon'
...     number = 7
...
>>> Favourite.food.value
bacon
>>> Favourite['number']
7
```

You can even go wild and mix things up (here we're using bit-fields via `bits`):

```python
>>> class Emphasis(Enum, values=bits, implicit=False):
...     with implicit:
...         underline, italic, bold
...     bold_italic = italic | bold
...
>>> Emphasis.bold_italic.value
6
```

### Aliases

By default, it is an error to repeat a value:

```python
>>> class Error(Enum, implicit=False, values=from_one):
...     with implicit:
...         one
...     another_one = 1
...
ValueError: Duplicate value (1) for one and another_one
```

but you can disable the safety check with `allow_aliases=True`:

```python
>>> class MulitlingualWeekday(Enum, implicit=False, values=from_one, allow_aliases=True):
...     with implicit:
...         monday, tuesday, wednesday, thursday, friday, saturday, sunday
...     lunes, martes, miercoles, jueves, viernes, sabado, domingo = \
...         monday, tuesday, wednesday, thursday, friday, saturday, sunday
...
```

This creates *aliases* - they are valid names, but they retrieve the original
tuple:

```python
>>> MulitlingualWeekday.lunes
MulitlingualWeekday(name='monday', value=1)
>>> MulitlingualWeekday['martes']
MulitlingualWeekday(name='tuesday', value=2)
```

Discussion
----------

### Background

Some time ago I wrote an
[intemperate rant](http://www.acooke.org/cute/Pythonssad0.html) about the
[standard Enum](http://www.python.org/dev/peps/pep-0435/) for Python 3.

Afterwards, I felt guilty.  So, to atone myself, I started to modify the
[code](https://bitbucket.org/stoneleaf/ref435), adding features that I felt
missing from the original.  The result was
[bnum](https://github.com/andrewcooke/bnum).

But, as I worked on bnum, I came to see that I was not producing the
consistent, elegant design that I was
[advocating](#https://github.com/andrewcooke/bnum#why-not-influence-the-official-design).
Instead, I was adding features to an already over-complex project.

So, after three weeks of work, I stopped.  The next day I wrote
[this](https://github.com/andrewcooke/simple-enum/blob/master/src/simplenum/__init__.py).

### Differences With Enum

This project differs from
[PEP-0345](http://www.python.org/dev/peps/pep-0435/)'s Enum in two important
ways.

1. The typical end-user will notice that the API defaults to implicit values.
This is because I feel the most common case for an Enum requires nothing more
than a set of names.  That case should be as simple as possible.

1. The Enum expert will see that I have made no effort to support other types
of enumeration (alternatives to named tuples) through inheritance.
In my career as a software engineer I have made many mistakes.  All too often
those mistakes involved inheritance.  This design reflects that experience.

In addition, this code supports alternative implicit values (eg. bit fields),
has no support for the "functional" form, and, by default, flags an error on
duplicates.

I realise that one day's work (even when born from three weeks of frustration)
is unlikely to have captured all the subtleties of the problem; that some of
the complexity of the standard Enum is justified and will, in time and with bug
fixes, clutter this project.  But I hope that I have found something of value
in the balance of features here, and that others will appreciate the view from
this particular local maximum of the design space.

### The Danger Of Magic

One objection to the implicit value approach used here is that it can lead
to confusing errors when global names are shadowed by implicit values.
However, this can be ameliorated in almost all cases by careful implementation.

In the case of implicit classes, like:

```python
>>> class Error1(Enum):
...     a = sin(b)
...
ExplicitError: Implicit scope support simple names only - no assignment or evaluation of expressions
```

the values returned are not the implicit values used, but `Explode`
instances which generate the given error on any access.  A similar error
is triggered by assignment.

The approach above, using a modified value, cannot be used for `with`
contexts, where the value might be used later.  But `with` contexts provide
a separate mechanism for detecting and modifying errors.  So here, for
example, a `TypeError` is detected and replaced:

```python
>>> class Error2(Enum, implicit=False):
...     with implicit:
...         a = sin(b)
...
ExplicitError: Implicit scope support simple names only - no assignment or evaluation of expressions
```

### Technical Details

The consistency of the two viewpoints (dict and named tuples) hinges on
the method `dict.items()`, which returns `(name, value)` tuples.  These
are both named tuples and the dictionary contents.

Implicit values are generated by providing a default value for missing
class dictionary contents.  This shadows global names so cannot be used
to evaluate expressions - but a simple list of names does not require any
evaluation.

Most of my Python programming (which I admit may be influenced by functional
languages) uses common, standard data structures.  An enumeration - an
immutable set of names, with an optional associated set of values - does not
require anything beyond that.  So "what is a good design?" reduces to "how
best can I fit enumerations into existing structures?"  A little consideration
gives two ways to associate names and values: in a dictionary, or as pairs.  A
little more consideration shows the two can be combined succinctly.  Hence the
design.

### Things You Can Do With The Simpler Enum (That You Can't Do With The Standard Enum)

Have a simple list of names in "class" form:

```python
>>> class Colour(Enum):
...     red
...     green
...     blue
```

Detect a stupid mistake:

```python
>>> class Error(Enum, values=from_one):
...     with implicit:
...         one
...         two
...     three = 2
...
ValueError: Duplicate value (2) for two and three
```

Define bit fields:

```python
>>> class IntEmphasis(Enum, values=bits):
...     underline
...     italic
...     bold
...
>>> allowed_styles = IntEmphasis.italic.value | IntEmphasis.bold.value
```

### Credits

Thanks to Ethan Furman, who graciously shared his code and so educated me on
the subtleties of the Python meta-class protocol.

[Duncan Booth](http://www.acooke.org/cute/Pythonssad0.html#Fri17May20131519040100)
provided the implicit values hack *and* the motivation to question authority.

Legalities
----------

(c) 2013 Andrew Cooke, [andrew@acooke.org](mailto://andrew@acooke.org);
released into the public domain for any use, but with absolutely no warranty.
