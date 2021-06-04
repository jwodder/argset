import pytest
from argset import ArgSet


def test_positional_only() -> None:
    a = ArgSet(
        required_positional_only=1,
        optional_positional_only=2,
        required_args=frozenset(),
        optional_args=frozenset(),
        takes_args=False,
        takes_kwargs=False,
    )
    assert a.positional_only == 3


def test_argnames() -> None:
    a = ArgSet(
        required_positional_only=0,
        optional_positional_only=0,
        required_args=frozenset(["foo", "bar"]),
        optional_args=frozenset(["baz"]),
        takes_args=False,
        takes_kwargs=False,
    )
    assert a.argnames == frozenset(["foo", "bar", "baz"])


def test_in_no_kwargs() -> None:
    a = ArgSet(
        required_positional_only=0,
        optional_positional_only=0,
        required_args=frozenset(["foo", "bar"]),
        optional_args=frozenset(["baz"]),
        takes_args=False,
        takes_kwargs=False,
    )
    assert "foo" in a
    assert "baz" in a
    assert "quux" not in a


def test_in_takes_kwargs() -> None:
    a = ArgSet(
        required_positional_only=0,
        optional_positional_only=0,
        required_args=frozenset(["foo", "bar"]),
        optional_args=frozenset(["baz"]),
        takes_args=False,
        takes_kwargs=True,
    )
    assert "foo" in a
    assert "baz" in a
    assert "quux" in a


def test_select_no_kwargs() -> None:
    a = ArgSet(
        required_positional_only=0,
        optional_positional_only=0,
        required_args=frozenset(["foo", "bar"]),
        optional_args=frozenset(["baz"]),
        takes_args=False,
        takes_kwargs=False,
    )
    assert a.select({"foo": 42, "baz": 23, "quux": 17}) == {"foo": 42, "baz": 23}


def test_select_takes_kwargs() -> None:
    a = ArgSet(
        required_positional_only=0,
        optional_positional_only=0,
        required_args=frozenset(["foo", "bar"]),
        optional_args=frozenset(["baz"]),
        takes_args=False,
        takes_kwargs=True,
    )
    assert a.select({"foo": 42, "baz": 23, "quux": 17}) == {
        "foo": 42,
        "baz": 23,
        "quux": 17,
    }


@pytest.mark.parametrize("takes_kwargs", [False, True])
def test_missing(takes_kwargs: bool) -> None:
    a = ArgSet(
        required_positional_only=0,
        optional_positional_only=0,
        required_args=frozenset(["foo", "bar"]),
        optional_args=frozenset(["baz", "gnusto"]),
        takes_args=False,
        takes_kwargs=takes_kwargs,
    )
    assert a.missing({"foo": 42, "baz": 23, "quux": 17}) == frozenset(["bar"])
