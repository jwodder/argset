from pathlib import Path
import sys
from typing import Any, Dict
import pytest
from argset import ArgSet, argset

DATA_DIR = Path(__file__).with_name("data")


@pytest.fixture(scope="module")
def pos_only() -> Dict[str, Any]:
    namespace: Dict[str, Any] = {}
    exec((DATA_DIR / "pos_only.py").read_text(), namespace)
    return namespace


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


@pytest.mark.skipif(
    sys.version_info[:2] < (3, 8), reason="Positional-only arguments not supported"
)
def test_pos_kwarg_only(pos_only: Dict[str, Any]) -> None:
    func = pos_only["pos_kwarg_only"]
    assert callable(func)
    assert argset(func) == ArgSet(
        required_positional_only=1,
        optional_positional_only=0,
        required_args=frozenset(["bar", "baz"]),
        optional_args=frozenset(),
        takes_args=False,
        takes_kwargs=False,
    )


@pytest.mark.skipif(
    sys.version_info[:2] < (3, 8), reason="Positional-only arguments not supported"
)
def test_pos_kwarg_only_defaults(pos_only: Dict[str, Any]) -> None:
    func = pos_only["pos_kwarg_only_defaults"]
    assert callable(func)
    assert argset(func) == ArgSet(
        required_positional_only=1,
        optional_positional_only=1,
        required_args=frozenset(),
        optional_args=frozenset(["baz", "quux"]),
        takes_args=False,
        takes_kwargs=False,
    )
