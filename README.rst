.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://github.com/jwodder/argset/workflows/Test/badge.svg?branch=master
    :target: https://github.com/jwodder/argset/actions?workflow=Test
    :alt: CI Status

.. image:: https://codecov.io/gh/jwodder/argset/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/argset

.. image:: https://img.shields.io/pypi/pyversions/argset.svg
    :target: https://pypi.org/project/argset/

.. image:: https://img.shields.io/github/license/jwodder/argset.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/argset>`_
| `PyPI <https://pypi.org/project/argset/>`_
| `Issues <https://github.com/jwodder/argset/issues>`_

``argset`` provides a simple interface for determining whether a callable takes
an argument with a given name, filtering a ``dict`` of potential arguments down
to just those that a callable accepts, and determining any required arguments
that are missing from a ``dict`` of potential arguments.

Installation
============
``argset`` requires Python 3.6 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install
``argset`` and its dependencies::

    python3 -m pip install argset


Examples
========

Inspecting a function's arguments::

    >>> from argset import argset
    >>> def my_func(foo, bar):
    ...     print(f"foo={foo!r}")
    ...     print(f"bar={bar!r}")
    ... 
    >>> a = argset(my_func)
    >>> "foo" in a
    True
    >>> "quux" in a
    False

Filtering a set of arguments to just those accepted by the function::

    >>> a.select({"foo": 42, "bar": 23, "quux": 17})
    {'foo': 42, 'bar': 23}
    >>> my_func(**a.select({"foo": 42, "bar": 23, "quux": 17}))
    foo=42
    bar=23

Same as above, but now the function takes ``**kwargs``::

    >>> from argset import argset
    >>> def my_func2(foo, **kwargs):
    ...     print(f"foo={foo!r}")
    ...     for k, v in kwargs.items():
    ...          print(f"{k}={v!r}")
    ... 
    >>> a2 = argset(my_func2)
    >>> "foo" in a2
    True
    >>> "quux" in a2
    True
    >>> a2.select({"foo": 42, "bar": 23, "quux": 17})
    {'foo': 42, 'bar': 23, 'quux': 17}
    >>> my_func2(**a2.select({"foo": 42, "bar": 23, "quux": 17}))
    foo=42
    bar=23
    quux=17


API
===

.. code:: python

    argset(func: Callable) -> ArgSet

Inspects a callable and returns a summary of its arguments as an ``ArgSet``

.. code:: python

    class ArgSet

A representation of the arguments taken by a callable.  It has the following
attributes & properties:

``required_positional_only: int``
    The number of arguments that are positional-only and do not have default
    values

``optional_positional_only: int``
    The number of arguments that are positional-only and have a default value

``positional_only: int``
    The total number of positional-only arguments

``required_args: frozenset[str]``
    The names of all positional-or-keyword or keyword-only arguments that do
    not have default values

``optional_args: frozenset[str]``
    The names of all positional-or-keyword or keyword-only arguments that have
    default values

``argnames: frozenset[str]``
    The names of all positional-or-keyword or keyword-only arguments

``takes_args: bool``
    Whether the callable has an argument of the form ``*args``

``takes_kwargs: bool``
    Whether the callable has an argument of the form ``**kwargs``

``ArgSet`` objects support the ``in`` operator; an expression of the form
``argname in a`` returns ``True`` iff ``argname`` is in ``a.argnames`` or
``a.takes_kwargs`` is ``True``.

``ArgSet`` objects have the following methods:

.. code:: python

    ArgSet.select(kwargs: Dict[str, Any]) -> Dict[str, Any]

Returns all items in ``kwargs`` where the key is the name of a
positional-or-keyword or keyword-only argument accepted by the callable.  If
``takes_kwargs`` is ``True``, the return value is a copy of ``kwargs``.

.. code:: python

    ArgSet.missing(kwargs: Dict[str, Any]) -> FrozenSet[str]

Returns all keys in ``required_args`` that do not appear in ``kwargs``
