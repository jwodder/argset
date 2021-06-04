"""
Simple callable argument inspection & filtering

Visit <https://github.com/jwodder/argset> for more information.
"""

__version__ = "0.1.0.dev1"
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
    required_positional_only: int
    optional_positional_only: int
    required_args: FrozenSet[str]
    optional_args: FrozenSet[str]
    takes_args: bool
    takes_kwargs: bool

    @property
    def positional_only(self) -> int:
        return self.required_positional_only + self.optional_positional_only

    @property
    def argnames(self) -> FrozenSet[str]:
        return self.required_args | self.optional_args

    def __contains__(self, arg: str) -> bool:
        return (
            self.takes_kwargs or arg in self.required_args or arg in self.optional_args
        )

    def select(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in kwargs.items() if k in self}

    def missing(self, kwargs: Dict[str, Any]) -> FrozenSet[str]:
        return frozenset(self.required_args - kwargs.keys())


def argset(func: Callable) -> ArgSet:
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
