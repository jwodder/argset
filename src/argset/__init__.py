"""
Simple callable argument inspection & filtering

``argset`` provides a simple interface for determining whether a callable takes
an argument with a given name, filtering a `dict` of potential arguments down
to just those that a callable accepts, and determining any required arguments
that are missing from a `dict` of potential arguments.

Visit <https://github.com/jwodder/argset> for more information.
"""

__version__ = "0.1.0"
__author__ = "John Thorvald Wodder II"
__author_email__ = "argset@varonathe.org"
__license__ = "MIT"
__url__ = "https://github.com/jwodder/argset"

from dataclasses import dataclass
import inspect
from typing import Any, Callable, Dict, FrozenSet

__all__ = ["ArgSet", "argset"]


@dataclass
class ArgSet:
    """A representation of the arguments taken by a callable"""

    #: The number of arguments that are positional-only and do not have default
    #: values
    required_positional_only: int

    #: The number of arguments that are positional-only and have a default
    #: value
    optional_positional_only: int

    #: The names of all positional-or-keyword or keyword-only arguments that do
    #: not have default values
    required_args: FrozenSet[str]

    #: The names of all positional-or-keyword or keyword-only arguments that
    #: have default values
    optional_args: FrozenSet[str]

    #: Whether the callable has an argument of the form ``*args``
    takes_args: bool

    #: Whether the callable has an argument of the form ``**kwargs``
    takes_kwargs: bool

    @property
    def positional_only(self) -> int:
        """The total number of positional-only arguments"""
        return self.required_positional_only + self.optional_positional_only

    @property
    def argnames(self) -> FrozenSet[str]:
        """The names of all positional-or-keyword or keyword-only arguments"""
        return self.required_args | self.optional_args

    def __contains__(self, arg: str) -> bool:
        return (
            self.takes_kwargs or arg in self.required_args or arg in self.optional_args
        )

    def select(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns all items in ``kwargs`` where the key is the name of a
        positional-or-keyword or keyword-only argument accepted by the
        callable.  If ``takes_kwargs`` is `True`, the return value is a copy of
        ``kwargs``.
        """
        return {k: v for k, v in kwargs.items() if k in self}

    def missing(self, kwargs: Dict[str, Any]) -> FrozenSet[str]:
        """
        Returns all keys in ``required_args`` that do not appear in ``kwargs``
        """
        return frozenset(self.required_args - kwargs.keys())


def argset(func: Callable) -> ArgSet:
    """
    Inspects a callable and returns a summary of its arguments as an `ArgSet`
    """
    sig = inspect.signature(func)
    required_pos = 0
    optional_pos = 0
    required_args = set()
    optional_args = set()
    takes_args = False
    takes_kwargs = False
    for param in sig.parameters.values():
        if param.kind is param.POSITIONAL_ONLY:
            if param.default is param.empty:
                required_pos += 1
            else:
                optional_pos += 1
        elif param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY):
            if param.default is param.empty:
                required_args.add(param.name)
            else:
                optional_args.add(param.name)
        elif param.kind is param.VAR_POSITIONAL:
            takes_args = True
        elif param.kind is param.VAR_KEYWORD:
            takes_kwargs = True
        else:
            raise AssertionError(
                "Unknown parameter type: {param.kind!r}"
            )  # pragma: no cover
    return ArgSet(
        required_positional_only=required_pos,
        optional_positional_only=optional_pos,
        required_args=frozenset(required_args),
        optional_args=frozenset(optional_args),
        takes_args=takes_args,
        takes_kwargs=takes_kwargs,
    )
