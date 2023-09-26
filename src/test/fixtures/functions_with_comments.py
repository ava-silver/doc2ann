def foo(bar):
    """
    this is a docstring

    Args:
        bar (int): something
    """

    # woah this is cool!
    return bar + 1


def baz(hi: str) -> None:
    x = 2
    # another comment, this time not as the first thing after the docstring

    print(hi * x)
