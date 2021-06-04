def pos_kwarg_only(foo, /, bar, *, baz):
    return foo


def pos_kwarg_only_defaults(foo, bar=None, /, baz=None, *, quux=None):
    return foo
