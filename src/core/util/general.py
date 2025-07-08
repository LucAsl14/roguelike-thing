from __future__ import annotations
from typing import Iterable, TypeVar, cast, Optional, Any, Type, Generic
from src.core.util.vector import Vec
from src.core.util.typing import *
from pathlib import Path
from math import floor
import weakref
import pygame
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
            yield (x, y)

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

def circle_surface(radius: int, color: Color) -> pygame.Surface:
    """Create a circular surface with a given radius and color.

    Args:
        radius: The radius of the circle.
        color: The color of the circle.

    Returns:
        A pygame.Surface with the given circle inscribed in it.
    """
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surface, color, (radius, radius), radius)
    return surface

def rect_surface(width: int, height: int, color: Color) -> pygame.Surface:
    """Create a rectangular surface with a given width, height, and color.

    Args:
        width: The width of the rectangle.
        height: The height of the rectangle.
        color: The color of the rectangle.

    Returns:
        A pygame.Surface of the specified size filled with the given color.
    """
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill(color)
    return surface

def square_surface(size: int, color: Color) -> pygame.Surface:
    """Create a square surface with a given size and color.

    Args:
        size: The size of the square.
        color: The color of the square.

    Returns:
        A pygame.Surface of the specified size filled with the given color.
    """
    return rect_surface(size, size, color)

__all__ = [
    "pathof",
    "ref_proxy",
    "read_file",
    "inttup",
    "sign",
    "iter_rect",
    "iter_square",
    "Singleton",
    "circle_surface",
    "rect_surface",
    "square_surface",
]
