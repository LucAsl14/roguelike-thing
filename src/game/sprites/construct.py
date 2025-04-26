from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell

class Construct(Spell):
    def __init__(self, scene: MainScene, charge_time: float, lifespan: float, hp: int) -> None:
        """
        Notes: \n
        A lifespan of -1 grants the construct infinite duration \n
        An hp amount of -1 makes it indestructible
        """
        super().__init__(scene, charge_time, "earth")
        self.lifespan = Timer(lifespan)
        self.endless = False
        if lifespan == -1: self.endless = True
        self.hp = hp
        self.pos: Vec
        self.angle: float
        self.scene.constructs.append(self)
        self.hitbox: Hitbox

    def update_charge(self, dt: float) -> None:
        pass
    def update_aiming(self, dt: float) -> None:
        pass

    def update_spell(self, dt: float) -> None:
        if self.is_colliding_player():
            self.collide_player()
        if not self.endless and self.lifespan.done:
            self.kill()
            return
        if self.hp == 0:
            self.kill()
        # if self.size == Vec(): Log.warn(f"This Construct ({self}) has no size and is likely causing lag")

    def trigger_spell(self) -> None:
        self.lifespan.reset()
        if self.aiming:
            self.pos = self.game.mouse_pos + self.scene.camera.pos
            super().trigger_spell()

    def collide_player(self) -> None:
        self.scene.player.vel = 100 * Vec((self.scene.player.pos - self.pos)).normalize()

    def take_damage(self, dmg: int) -> int:
        """
        Returns:
            actual damage taken
        """
        if self.aiming:
            return 0
        prev_hp = self.hp
        if self.hp == -1: return dmg
        self.hp = max(self.hp - dmg, 0)
        return prev_hp - self.hp

    def kill(self) -> None:
        if not self.killed:
            self.scene.constructs.remove(self)
        super().kill()

    def is_colliding_player(self) -> bool:
        if self.scene.player.pos.distance_to(self.pos) < self.size.magnitude() + self.scene.player.size.magnitude() \
        and self.hitbox.is_colliding(self.scene.player.hitbox):
            return True
        return False
