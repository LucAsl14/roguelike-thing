from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell
from .construct import Construct

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .enemy import Enemy
    from .player import Player
    from .entity import Entity
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
                 origin: str,
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
        self.origin = origin
        self.max_dmg_per_target = max_damage_per_target
        self.ignore_elem = []
        self.scene.projectiles.append(self)

    def kill(self) -> None:
        if not self.killed:
            self.scene.projectiles.remove(self)
        super().kill()

    def update_charge(self, dt: float) -> None:
        pass

    def get_nearby_entities(self) -> list[Entity]:
        cx, cy = self.scene.spacial_hash_key(self.pos)
        nearby: list[Entity] = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nearby.extend(self.scene.collideable_buckets.get(Vec(cx+dx, cy+dy), {}).get("entity", []))
        return nearby

    def get_nearby_constructs(self) -> list[Construct]:
        cx, cy = self.scene.spacial_hash_key(self.pos)
        nearby: list[Construct] = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nearby.extend(self.scene.collideable_buckets.get(Vec(cx+dx, cy+dy), {}).get("construct", []))
        return nearby

    def get_nearby_projectiles(self) -> list[Projectile]:
        cx, cy = self.scene.spacial_hash_key(self.pos)
        nearby: list[Projectile] = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nearby.extend(self.scene.collideable_buckets.get(Vec(cx+dx, cy+dy), {}).get("projectile", []))
        return nearby

    def update_spell(self, dt: float) -> None:
        self.vel += self.external_acc
        self.pos += self.vel * dt
        self.external_acc = Vec()

        self.hitbox.set_position(self.pos)

        if self.lifespan.done:
            self.kill()
            return
        # collision with anything collidable
        for construct in self.get_nearby_constructs():
            if self.pos.distance_to(construct.pos) < self.rad + construct.size.magnitude() \
               and self.hitbox.is_colliding(construct.hitbox):
                self.collide(construct)
        for projectile in self.get_nearby_projectiles():
            if self.pos.distance_to(projectile.pos) < self.rad + projectile.rad \
               and projectile.element not in self.ignore_elem \
               and projectile != self and self.hitbox.is_colliding(projectile.hitbox):
                self.collide(projectile)
        from .enemy import Enemy
        if self.origin != "enemy":
            for enemy in self.get_nearby_entities():
                if isinstance(enemy, Enemy):
                    if self.pos.distance_to(enemy.pos) < self.rad + enemy.size.magnitude() \
                    and self.hitbox.is_colliding(enemy.hitbox):
                        self.collide(enemy)
        if self.origin != "player":
            player = self.scene.player
            if player.pos.distance_to(self.pos) < self.rad + player.size.magnitude() \
               and self.hitbox.is_colliding(player.hitbox):
                self.collide(player)

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

    def collide(self, target: Construct | Projectile | Enemy | Player) -> None:
        if isinstance(target, type(self)): return # prevent self-collision (we might want this?)
        dmg_dealt = min(self.max_dmg_per_target, target.take_damage(self.damage))
        self.take_damage(dmg_dealt)
        if dmg_dealt > 0:
            Log.debug(f"{self} dealt {dmg_dealt} dmg to {target}")
