from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from client.core.scene import Scene

from abc import ABC as AbstractClass, abstractmethod
from uuid import uuid4
from util import *
import pygame

class Sprite(AbstractClass):
    def __init__(self, scene: Scene, layer: str) -> None:
        self.uuid = str(uuid4())
        self.game = ref_proxy(scene.game)
        self.scene = ref_proxy(scene)
        self.layer = layer
        self.pos = Vec()
        self.size = Vec()

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, target: pygame.Surface) -> None:
        pass

    @property
    def center_pos(self) -> Vec:
        return self.pos + self.size / 2

    @property
    def screen_pos(self) -> Vec:
        if not hasattr(self.scene, "camera"):
            return self.pos
        return self.pos - self.scene.camera.pos # type: ignore

    @property
    def screen_center_pos(self) -> Vec:
        return self.screen_pos + self.size / 2

    def kill(self) -> None:
        self.scene.remove(self)

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}{{{self.uuid}}}"
