from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell
from .entity import Entity
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

    def update_spell(self, dt: float) -> None:
        if len((entities := self.colliding_entities())) > 0:
            self.collide(entities, dt)
        if not self.endless and self.lifespan.done:
            self.kill()
            return
        if self.hp == 0:
            self.kill()
        # if self.size == Vec(): Log.warn(f"This Construct ({self}) has no size and is likely causing lag")

    def collide(self, entities: list[Entity], dt: float) -> None:
        for entity in entities:
            normal = Vec((entity.pos - self.pos)).normalize()
            entity.ext_acc += 5000 * normal * dt
            entity.vel -= entity.vel.project(normal)
            entity.vel *= 5e-9 ** dt

    def take_damage(self, dmg: int) -> int:
        """
        Returns:
            actual damage taken
        """
        prev_hp = self.hp
        if self.hp == -1: return dmg
        self.hp = max(self.hp - dmg, 0)
        return prev_hp - self.hp

    def kill(self) -> None:
        if not self.killed:
            self.scene.constructs.remove(self)
        super().kill()

    def colliding_entities(self) -> list[Entity]:
        entities = []
        if self.pos.distance_to(self.scene.player.pos) > 1500: return entities
        self_rad = (self.size.x + self.size.y) / 2

        def is_close(other: Entity) -> bool:
            other_rad = (other.size.x + other.size.y) / 2
            return other.pos.distance_squared_to(self.pos) < (self_rad + other_rad) ** 2
        # the player
        if is_close(self.scene.player) and self.hitbox.is_colliding(self.scene.player.hitbox):
            entities.append(self.scene.player)
        # enemies
        for enemy in self.scene.enemies:
         if is_close(enemy) and self.hitbox.is_colliding(enemy.hitbox):
            entities.append(enemy)

        return entities
