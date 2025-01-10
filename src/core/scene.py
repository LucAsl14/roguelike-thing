from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from abc import ABC as AbstractClass, abstractmethod
from src.core.sprite_manager import SpriteManager
from src.core.sprite import Sprite
from src.core.util import *
import pygame

class Scene(AbstractClass):
    def __init__(self, game: Game) -> None:
        self.game = ref_proxy(game)
        self.sprite_manager = SpriteManager()

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass

    def add(self, sprite: Sprite) -> None:
        self.sprite_manager.add(sprite)

    def remove(self, sprite: Sprite) -> None:
        try:
            self.sprite_manager.remove(sprite)
        except ValueError:
            Log.warn(f"Attempted to remove sprite {sprite} from scene {self}, but it was not found in the sprite manager.")

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self.game = self.game.__class__()
