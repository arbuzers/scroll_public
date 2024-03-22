import asyncio
import multiprocessing
import threading


class ArbitraryAttributes:
    """A class that can be assigned arbitrary attributes."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class AutoRepr:
    """Contains a __repr__ function that automatically builds the output of a class using all its variables."""

    def __repr__(self) -> str:
        values = ('{}={!r}'.format(key, value) for key, value in vars(self).items())
        return '{}({})'.format(self.__class__.__name__, ', '.join(values))


class Singleton:
    """A class that implements the singleton pattern."""
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls)

        return cls._instances[cls]


class SingletonWithLock:
    """A class that implements the singleton pattern with the lock."""
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(SingletonWithLock, cls).__new__(cls)

        return cls._instances[cls]


class SingletonThreading(SingletonWithLock):
    """A class that implements the singleton pattern with the threading lock."""
    pass


class SingletonMultiprocessing(SingletonWithLock):
    """A class that implements the singleton pattern with the multiprocessing lock."""
    _lock = multiprocessing.Lock()


class SingletonAsyncio(SingletonWithLock):
    """A class that implements the singleton pattern with the asyncio lock."""
    _lock = asyncio.Lock()
