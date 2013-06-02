simple-enum
===========

A simpler Enum for Python.

* [Getting Started](#getting-started)
  * [The Dictionary Point Of View](#the-dictionary-point-of-view)
  * [The Named Tuple Point Of View](#the-named-tuple-point-of-view)
  * [That's It, Really](#thats-it-really)

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

As before, you can change the values:

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

OK, so there is some more below.  But the above should be all you need in
most cases.
