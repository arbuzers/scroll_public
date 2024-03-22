def randbool() -> bool:
    """Return a random bool."""
    from random import getrandbits

    return bool(getrandbits(1))
