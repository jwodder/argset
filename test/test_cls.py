from argset import ArgSet

def test_positional_only() -> None:
    a = ArgSet(required_positional_only=1, optional_positional_only=2, required_args=frozenset(), optional_args=frozenset(), takes_kwargs=False)
    assert a.positional_only == 3

def test_argnames() -> None:
    a = ArgSet(required_positional_only=0, optional_positional_only=0, required_args=frozenset(["foo", "bar"]), optional_args=frozenset(["baz"]), takes_kwargs=False)
    assert a.argnames == frozenset(["foo", "bar", "baz"])

def test_in_no_kwargs() -> None:
    a = ArgSet(required_positional_only=0, optional_positional_only=0, required_args=frozenset(["foo", "bar"]), optional_args=frozenset(["baz"]), takes_kwargs=False)
    assert "foo" in a
    assert "baz" in a
    assert "quux" not in a

def test_in_takes_kwargs() -> None:
    a = ArgSet(required_positional_only=0, optional_positional_only=0, required_args=frozenset(["foo", "bar"]), optional_args=frozenset(["baz"]), takes_kwargs=True)
    assert "foo" in a
    assert "baz" in a
    assert "quux" in a
