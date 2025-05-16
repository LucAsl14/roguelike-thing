from __future__ import annotations
from src.core import *
from .entity import Entity
from abc import abstractmethod
class Enemy(Entity):
    def __init__(self, scene: MainScene, hp: int, pos: Vec) -> None:
        super().__init__(scene, hp, pygame.transform.rotate(Image.get("test"), 180), pos)
        self.scene = scene
        self.scene.enemies.append(self)
        self.killed = False

    def update(self, dt: float) -> None:
        self.update_movement(dt)
        self.update_attack(dt)
        self.update_position(dt)
        self.collide_enemies()
        if self.hp <= 0:
            self.kill()
            return

    @abstractmethod
    def update_movement(self, dt: float):
        pass

    def update_attack(self, dt: float):
        pass

    def kill(self):
        if not self.killed:
            self.scene.enemies.remove(self)
            super().kill()
            self.killed = True

    def get_player_direction(self) -> float:
        return atan2(self.scene.player.pos.y - self.pos.y, self.scene.player.pos.x - self.pos.x)

    def get_player_distance(self) -> float:
        return self.scene.player.pos.distance_to(self.pos)

    def collide_enemies(self) -> None:
        for enemy in self.scene.enemies:
         if enemy != self and enemy.pos.distance_to(self.pos) < self.size.magnitude() + enemy.size.magnitude() \
         and self.hitbox.is_colliding(enemy.hitbox):
            enemy.vel = 100 * Vec((enemy.pos - self.pos)).normalize()

    def is_colliding_player(self) -> bool:
        if self.scene.player.pos.distance_to(self.pos) < self.size.magnitude() + self.scene.player.size.magnitude() \
        and self.hitbox.is_colliding(self.scene.player.hitbox):
            return True
        return False
