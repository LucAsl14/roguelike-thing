from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from src.core.render_layer import Layer, LayerGroup, LayerGroupRecord
from abc import ABC as AbstractClass, abstractmethod
from src.core.sprite import Sprite
from typing import ClassVar
from src.core.util import *
import pygame

class Scene(AbstractClass):
    _layers: ClassVar[list[LayerGroupRecord]] = []

    def __init__(self, game: Game) -> None:
        self.game = ref_proxy(game)
        self.layer_groups = [
            *map(lambda group: group.construct(self), self._layers),
        ]
        self.layers = {layer.name: layer for group in self.layer_groups for layer in group.layers}

    def preupdate(self, dt: float) -> None:
        pass

    def postupdate(self, dt: float) -> None:
        pass

    def update(self, dt: float) -> None:
        self.preupdate(dt)
        for layer in self.layers.values():
            layer.update(dt)
        self.postupdate(dt)

    def predraw(self, screen: pygame.Surface) -> None:
        pass

    def postdraw(self, screen: pygame.Surface) -> None:
        pass

    def draw(self) -> None:
        for group in self.layer_groups:
            group.surface.fill((0, 0, 0, 0))
        self.predraw(self.layer_groups[0].surface)
        for group in self.layer_groups[:-1]:
            group.draw()
        if Debug.on():
            self.layer_groups[-1].draw(self.postdraw, Debug.draw)
        else:
            self.layer_groups[-1].draw(self.postdraw)

    def add(self, sprite: Sprite) -> None:
        self.layers[sprite.layer].add(sprite)

    def remove(self, sprite: Sprite) -> None:
        try:
            self.layers[sprite.layer].remove(sprite)
        except ValueError:
            Log.warn(f"Attempted to remove sprite {sprite} from scene {self}, but it was not found in the scene.")
