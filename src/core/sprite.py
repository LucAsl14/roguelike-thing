from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.settings import Layer
    from src.core.scene import Scene

from abc import ABC as AbstractClass, abstractmethod
from src.core.util import *
from typing import Self
from uuid import uuid4
import pygame

class Sprite(AbstractClass):
    def __init__(self, scene: Scene, layer: Layer) -> None:
        self.uuid = uuid4()
        self.game = ref_proxy(scene.game)
        self.scene = ref_proxy(scene)
        self.layer = layer

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass

    def bind(self, sprite: Self) -> None:
        self.scene.sprite_manager.layers[self.layer].bind(sprite, self)

    def kill(self) -> None:
        self.scene.sprite_manager.remove(self)

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}{{{self.uuid}}}"

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        # Jesus Christ this is an ugly hack
        # But uh, without this, when the sprite is unpickled, the game attr no
        # longer points to the correct game instance, so we need to update it
        # by retrieving the singleton instance accessed through the unpickled
        # game instance, since we cannot import the Game class here
        self.game = self.game.__class__()
