simple-enum
===========

A simpler Enum for Python.

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

but you can easily change that:

```python
>>> class Weekday(Enum, values=from_one):
...     monday, tuesday, wednesday, thursday, friday, saturday, sunday
...
>>> Weekday['monday']
1
```

