from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell
from .construct import Construct

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .enemy import Enemy
class Projectile(Spell):
    def __init__(self,
                 scene: MainScene,
                 target_posdiff: Vec,
                 lifespan: float,
                 speed: float,
                 charge_time: float,
                 dmg: int,
                 elem: str,
                 radius: int,
                 max_damage_per_target: int = 9999) -> None:
        super().__init__(scene, charge_time, elem)
        self.vel = target_posdiff.normalize() * speed
        self.external_acc = Vec()
        self.pos = self.scene.player.pos.copy()
        self.speed = speed
        self.lifespan = Timer(lifespan)
        self.rad = radius
        self.damage = dmg
        self.hitbox = Hitbox(self.pos, [])
        self.hitbox.set_size_rad(radius)
        self.max_dmg_per_target = max_damage_per_target
        self.ignore_elem = []
        self.scene.projectiles.append(self)

    def kill(self) -> None:
        if not self.killed:
            self.scene.projectiles.remove(self)
        super().kill()

    def update_charge(self, dt: float) -> None:
        pass

    def update_spell(self, dt: float) -> None:
        self.vel += self.external_acc
        self.pos += self.vel * dt
        self.external_acc = Vec()

        self.hitbox.set_position(self.pos)

        if self.lifespan.done:
            self.kill()
            return
        # collision with anything collidable
        for construct in self.scene.constructs:
            if self.pos.distance_to(construct.pos) < self.rad + construct.size.magnitude() and \
               self.hitbox.is_colliding(construct.hitbox):
                self.collide(construct)
        for projectile in self.scene.projectiles:
            if self.pos.distance_to(projectile.pos) < self.rad + projectile.rad and \
               projectile.element not in self.ignore_elem and \
               projectile != self and self.hitbox.is_colliding(projectile.hitbox):
                self.collide(projectile)
        for enemy in self.scene.enemies:
            if self.pos.distance_to(enemy.pos) < self.rad + enemy.size.magnitude() and \
            self.hitbox.is_colliding(enemy.hitbox):
                self.collide(enemy)

    def take_damage(self, dmg: int) -> int:
        """
        Returns:
            Amount of damage taken
        """
        prev_dmg = self.damage
        self.damage -= dmg
        if self.damage <= 0:
            self.damage = 0
            self.kill()
        return prev_dmg - self.damage

    def collide(self, target: Construct | Projectile | Enemy) -> None:
        if isinstance(target, type(self)): return # prevent self-collision (we might want this?)
        dmg_dealt = min(self.max_dmg_per_target, target.take_damage(self.damage))
        self.take_damage(dmg_dealt)
        if dmg_dealt > 0:
            Log.debug(f"{self} dealt {dmg_dealt} dmg to {target}")
