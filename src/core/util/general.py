from __future__ import annotations

from typing import Iterable, TypeVar, cast, Optional, Any, Type, Generic
from src.core.util.vector import Vec
from src.core.util.typing import *
from pathlib import Path
from math import floor
import weakref
import sys
import os

T = TypeVar("T")
BUNDLE_DIR = getattr(
    sys, "_MEIPASS",
    Path(os.path.abspath(os.path.dirname(__file__))).parent
)

def pathof(file: str) -> str:
    """Gets the path to the given file that will work with exes.
    Args:
        file (str): The original path to go to
    Returns:
        str: The bundled - exe compatible file path
    """

    abspath = os.path.abspath(os.path.join(BUNDLE_DIR, file))
    if not os.path.exists(abspath):
        abspath = file
    return abspath

def ref_proxy(obj: T) -> T:
    """Create a weak reference proxy to an object if it isn"t already one.

    Args:
        obj: The object to create a weak reference proxy to.

    Returns:
        The weak reference proxy.
    """
    if isinstance(obj, weakref.ProxyTypes):
        return obj
    return weakref.proxy(obj)

def read_file(path: str) -> str:
    """Opens a file, read the contents of the file, then closes it.

    Args:
        path: The path of the file to read from.

    Returns:
        The full contents of the file.
    """
    with open(path, "r") as file:
        return file.read()

def inttup(tup: Coord) -> tuple:
    """Convert a tuple of 2 numbers to a tuple of 2 ints.

    This uses the floor function to convert the numbers to ints.

    Args:
        tup: The tuple to convert.

    Returns:
        The integer tuple.
    """
    return (floor(tup[0]), floor(tup[1]))

def sign(x: float) -> int:
    """Get the sign of a number.

    Args:
        x: The number to get the sign of.

    Returns:
        The sign of the number.
    """
    return (x > 0) - (x < 0)

def iter_rect(left: int, right: int, top: int, bottom: int) -> Iterable[IntCoord]:
    """Iterate over the coordinates of a rectangle.

    Args:
        left: The leftmost x-coordinate (inclusive).
        right: The rightmost x-coordinate (inclusive).
        top: The topmost y-coordinate (inclusive).
        bottom: The bottommost y-coordinate (inclusive).

    Yields:
        The coordinates of the rectangle.
    """
    for x in range(int(left), int(right) + 1):
        for y in range(int(top), int(bottom) + 1):
            yield cast(IntCoord, Vec(x, y))

def iter_square(size: int) -> Iterable[IntCoord]:
    """Iterate over the coordinates of a square.

    Args:
        size: The size of the square.

    Yields:
        The coordinates of the square.
    """
    yield from iter_rect(0, size - 1, 0, size - 1)

T = TypeVar("T")
U = TypeVar("U")

class Singleton(Generic[T], type):
    """A metaclass that ensures a class is a singleton."""
    _instance: Optional[T] = None

    def __call__(cls: Singleton[T], *args: Any, **kwargs: Any) -> T:
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cast(T, cls._instance)

class Storage(Generic[T, U], type):
    """A metaclass that ensures a class is a singleton and redirects class
    attribute access to the singleton instance. Effectively, this metaclass
    makes the class a storage for a bunch of attributes that can be more easily
    accessed without needing to manually instantiate the class.
    """
    _instance: Optional[T] = None

    def __call__(cls: Storage[T, U], *args: Any, **kwargs: Any) -> T:
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cast(T, cls._instance)

    def __getattr__(cls: Storage[T, U], name: str) -> U:
        if cls._instance is None:
            cls._instance = cls()
        return getattr(cls._instance, name)

__all__ = [
    "pathof",
    "ref_proxy",
    "read_file",
    "inttup",
    "sign",
    "iter_rect",
    "iter_square",
    "Singleton",
    "Storage",
]
