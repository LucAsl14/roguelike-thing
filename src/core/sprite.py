from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.scene import Scene

from abc import ABC as AbstractClass, abstractmethod
from src.core.util import *
from uuid import uuid4
import pygame

class Sprite(AbstractClass):
    def __init__(self, scene: Scene, layer: str) -> None:
        self.uuid = uuid4()
        self.game = ref_proxy(scene.game)
        self.scene = ref_proxy(scene)
        self.layer = layer

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, target: pygame.Surface) -> None:
        pass

    def kill(self) -> None:
        self.scene.remove(self)

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}{{{self.uuid}}}"
