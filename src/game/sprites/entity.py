from __future__ import annotations
from src.core import *
from pygame import Surface

class Entity(Sprite):
    def __init__(self, scene: MainScene, hp: int, image: Surface, pos: Vec) -> None:
        super().__init__(scene, "DEFAULT")

        # combat
        self.hp = hp

        # movement-related variables
        self.pos = pos
        self.vel = Vec()
        self.acc = Vec()
        self.ext_acc = Vec()

        # visuals
        self.image = image
        rect = self.image.get_rect()
        self.hitbox = Hitbox(self.pos, [])
        self.hitbox.set_size_rect(rect.width, rect.height)
        self.size = Vec(rect.width, rect.height)
        self.angle = 0


    def update_position(self, dt: float) -> None:
        self.vel += self.acc * dt
        self.vel += self.ext_acc
        self.ext_acc = Vec()
        self.vel *= 0.004 ** dt
        self.pos += self.vel * dt
        self.hitbox.set_position(self.pos)
        self.hitbox.set_rotation(self.angle)

    def take_damage(self, dmg: int) -> int:
        prev_hp = self.hp
        self.hp -= dmg
        return prev_hp - self.hp

    def draw(self, target: pygame.Surface) -> None:
        target.blit(self.image, self.screen_pos - Vec(self.image.get_rect().size) / 2)
