"""
Simple callable argument inspection & filtering

Visit <https://github.com/jwodder/argset> for more information.
"""

__version__ = "0.1.0.dev1"
__author__ = "John Thorvald Wodder II"
__author_email__ = "argset@varonathe.org"
__license__ = "MIT"
__url__ = "https://github.com/jwodder/argset"

from typing import FrozenSet, NamedTuple


class ArgSet(NamedTuple):
    required_positional_only: int
    optional_positional_only: int
    required_args: FrozenSet[str]
    optional_args: FrozenSet[str]
    takes_kwargs: bool
