from typing import Any, Dict
from argset import ArgSet, argset


def test_simple() -> None:
    def simple(foo: Any) -> Any:
        return foo

    assert argset(simple) == ArgSet(
        required_positional_only=0,
        optional_positional_only=0,
        required_args=frozenset(["foo"]),
        optional_args=frozenset(),
        takes_args=False,
        takes_kwargs=False,
    )


def test_defaulting() -> None:
    def defaulting(foo: Any, bar: Any = None) -> Any:
        return foo

    assert argset(defaulting) == ArgSet(
        required_positional_only=0,
        optional_positional_only=0,
        required_args=frozenset(["foo"]),
        optional_args=frozenset(["bar"]),
        takes_args=False,
        takes_kwargs=False,
    )


def test_kwarged() -> None:
    def kwarged(**kwargs: Any) -> Dict[str, Any]:
        return kwargs

    assert argset(kwarged) == ArgSet(
        required_positional_only=0,
        optional_positional_only=0,
        required_args=frozenset(),
        optional_args=frozenset(),
        takes_args=False,
        takes_kwargs=True,
    )


def test_arged() -> None:
    def arged(*args: Any) -> tuple:
        return args

    assert argset(arged) == ArgSet(
        required_positional_only=0,
        optional_positional_only=0,
        required_args=frozenset(),
        optional_args=frozenset(),
        takes_args=True,
        takes_kwargs=False,
    )
