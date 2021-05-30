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
from typing import FrozenSet


@dataclass
class ArgSet:
    required_positional_only: int
    optional_positional_only: int
    required_args: FrozenSet[str]
    optional_args: FrozenSet[str]
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
