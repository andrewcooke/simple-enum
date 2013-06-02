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
* [Discussion](#discussion)
  * [Background](#background)
  * [Differences With Enum](#differences-with-enum)
  * [Credits](#credits)

Getting Started
---------------

```sh
easy_install simple-enum
```

### The Dictionary Point Of View

An Enum is an ordered, immutable dictionary:

```python
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

By default, the values in the dictionary are the names:

```python
>>> Colour['red']
'red'
```

but you can change that using `values`:

```python
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

Discussion
----------

### Background

Some time ago I wrote an
[intemperate rant](#http://www.acooke.org/cute/Pythonssad0.html) about the
[standard Enum](http://www.python.org/dev/peps/pep-0435/) for Python 3.

Afterwards, I felt guilty.  So, to atone myself, I started to modify the
[code](https://bitbucket.org/stoneleaf/ref435), adding features that I felt
missing from the original.  The result was
[bnum](https://github.com/andrewcooke/bnum).

But, as I worked on bnum, I came to see that I was not producing the
consistent, elegant design that I was
[advocating](#https://github.com/andrewcooke/bnum#why-not-influence-the-official-design).
Instead, I was adding features to an already over-complex project.

So, after three weeks of work, I stopped.  The next day I wrote this.

### Differences With Enum

This project different from
[PEP-0345](http://www.python.org/dev/peps/pep-0435/)'s Enum in two important
ways.

The typical end-user will notice that the API defaults to implicit values.
This is because I feel the most common case for an Enum requires nothing more
than a set of names.  That case should be as simple as possible.

The Enum expert will see that I have made no effort to support inheritance.
In my career as a software engineer I have made many mistakes.  All too often
those mistakes involved inheritance.  This design reflects that experience.

I realise that one day's work is unlikely to have captured all the subtleties
of the problem; that some of the complexity of the standard Enum is
justified and will, in time and with bug fixes, clutter this project.  But I
hope that I have found something of value in the balance of features here, and
that others will appreciate the view from this particular local maximum of
the design space.

### Credits

Thanks to Ethan Furman, who graciously shared his code and so educated me on
the subtleties of Python meta-class protocols.
