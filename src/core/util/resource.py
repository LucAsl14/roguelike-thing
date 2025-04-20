from __future__ import annotations
from src.core.util.general import pathof, read_file
from typing import TypeVar, Generic, Any, ClassVar
from src.core.util.debug import Log
from dataclasses import dataclass
from abc import abstractmethod
import pygame
import os

class ResourceMeta(type):
    def __init__(cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]) -> None:
        super().__init__(name, bases, dct)

        if not hasattr(cls, "DIR"):
            raise AttributeError(f"Resource class {cls.__name__} must have a 'DIR' attribute.")

        # Append subclass directory to parent's base directory
        for base in bases:
            if not hasattr(base, "DIR"): continue
            cls.DIR = pathof(os.path.join(base.DIR, cls.DIR))
            break

        # Create copy of instances for each subclass
        cls.instances = {}

T = TypeVar("T")
@dataclass
class Resource(Generic[T], metaclass=ResourceMeta):
    """A resource loaded from disk."""
    DIR = "res"
    instances: ClassVar[dict[str, Resource]] = {}

    @classmethod
    def preload(cls) -> int:
        """Preload all resources."""
        loaded = 0
        for subclass in cls.__subclasses__():
            loaded += subclass.preload()
        for instance in cls.instances.values():
            cls.get(instance.name)
        loaded += len(cls.instances)
        Log.info(f"Preloaded {loaded} {cls.__name__}s.")
        return loaded

    @classmethod
    def get(cls, name: str) -> T:
        instance = cls.instances[name]
        if instance.object is None:
            instance.object = instance.load()
        return instance.object

    name: str
    path: str

    def __post_init__(self) -> None:
        self.path = os.path.join(self.DIR, self.path)
        self.object = None
        self.instances[self.name] = self

    @abstractmethod
    def load(self) -> T:
        """Load the resource from disk."""
        pass

@dataclass
class Image(Resource[pygame.Surface]):
    """An image resource."""
    DIR = "images"

    scale: float = 1.0

    def load(self) -> pygame.Surface:
        surface = pygame.image.load(self.path).convert_alpha()
        return pygame.transform.scale_by(surface, self.scale)

@dataclass
class Sound(Resource[pygame.Sound]):
    """A sound resource."""
    DIR = "sounds"

    volume: float = 1.0

    def load(self) -> pygame.Sound:
        sound = pygame.Sound(self.path)
        sound.set_volume(self.volume)
        return sound

@dataclass
class Font(Resource[pygame.Font]):
    """A font resource."""
    DIR = "fonts"

    size: int
    bold: bool = False
    italic: bool = False
    underline: bool = False
    striketrough: bool = False

    def load(self) -> pygame.Font:
        font = pygame.Font(self.path, self.size)
        font.set_bold(self.bold)
        font.set_italic(self.italic)
        font.set_underline(self.underline)
        font.set_strikethrough(self.striketrough)
        return font

@dataclass
class VertShader(Resource[str]):
    """A vertex shader resource."""
    DIR = "shaders"

    def load(self) -> str:
        return read_file(self.path)

@dataclass
class FragShader(Resource[str]):
    """A fragment shader resource."""
    DIR = "shaders"

    def load(self) -> str:
        return read_file(self.path)

__all__ = [
    "Resource",
    "Image",
    "Sound",
    "Font",
    "VertShader",
    "FragShader",
]
