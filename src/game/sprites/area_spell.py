from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player
class AreaSpell(Spell):
    def __init__(self, scene: MainScene, target_posdiff: Vec, charge_time: float, elem: str, lifespan: float, radius: int, layer: str = "DEFAULT") -> None:
        super().__init__(scene, charge_time, elem, layer)
        self.lifespan = Timer(lifespan)
        self.rad = radius
        self.pos = target_posdiff + self.scene.player.pos

    def update_charge(self, dt: float) -> None:
        pass

    def update_spell(self, dt: float) -> None:
        if self.lifespan.done:
            self.kill()
