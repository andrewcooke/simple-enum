simple-enum
===========

A simpler Enum for Python.

* [Getting Started](#getting-started)
  * [The Dictionary Point Of View](#the-dictionary-point-of-view)
  * [The Named Tuple Point Of View](#the-named-tuple-point-of-view)
  * [That's It, Really](#thats-it-really)
* [Advanced Use](#advanced-use)
  * [Retrieving Tuples](#retrieving-tuples)
  * [Providing Implicit Values](#providing-implicit-values)
  * [Providing Explicit Values](#providing-explicit-values)

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
