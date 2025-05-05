from __future__ import annotations
from src.core import *
from abc import abstractmethod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player
class Spell(Sprite):
    def __init__(self, scene: MainScene, charge_time: float, elem: str, layer: str = "DEFAULT", cooldown: float = 0) -> None: # cooldown is very much temporary
        super().__init__(scene, layer)
        # self.aiming = True
        self.scene = scene
        self.charging_time = Timer(charge_time)
        self.element = elem
        self.killed = False

    def update(self, dt: float) -> None:
        if self.killed:
            return
        if not self.charging_time.done:
            self.update_charge(dt)
        else:
            self.update_spell(dt)

    def draw(self, target: pygame.Surface) -> None:
        if not self.charging_time.done:
            self.draw_charge(target)
        if self.pos.distance_to(self.scene.player.pos) > 800: return
        if self.charging_time.done:
            self.draw_spell(target)

    def kill(self) -> None:
        if not self.killed:
            super().kill()
        self.killed = True

    @abstractmethod
    def draw_spell(self, screen: pygame.Surface) -> None:
        pass

    @abstractmethod
    def draw_charge(self, screen: pygame.Surface) -> None:
        pass

    @abstractmethod
    def update_spell(self, dt: float) -> None:
        pass

    @abstractmethod
    def update_charge(self, dt: float) -> None:
        pass

    def trigger_spell(self) -> None:
        pass
