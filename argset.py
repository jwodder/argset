from typing import FrozenSet, NamedTuple

class ArgSet(NamedTuple):
    required_positional_only: int
    optional_positional_only: int
    required_args: FrozenSet[str]
    optional_args: FrozenSet[str]
    takes_kwargs: bool
