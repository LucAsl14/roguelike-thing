from __future__ import annotations
from src.core import *
from pygame import Surface

class Entity(Sprite):
    def __init__(self, scene: MainScene, hp: int, image: Surface, pos: Vec) -> None:
        super().__init__(scene, "DEFAULT")

        self.scene = scene

        # combat
        self.hp = hp

        # movement-related variables
        self.pos = pos
        self.vel = Vec()
        self.acc = Vec()
        self.ext_acc = Vec()
        self.ext_vel = Vec()

        # visuals
        self.image = image
        rect = self.image.get_rect()
        self.hitbox = Hitbox(self.pos, [])
        self.hitbox.set_size_rect(rect.width, rect.height)
        self.size = Vec(rect.width, rect.height)
        self.angle = 0


    def update_position(self, dt: float) -> None:
        # All of vel, acc, ext_vel, etc. are measured in unit/s
        for entity in self.colliding_entities():
            entity.ext_acc += 6000 * Vec((entity.pos - self.pos)).normalize() * dt
        self.vel += self.acc * dt
        self.vel += self.ext_acc
        self.ext_acc = Vec()
        self.vel *= 0.004 ** dt
        self.pos += self.vel * dt
        self.pos += self.ext_vel
        self.ext_vel = Vec()
        self.hitbox.set_position(self.pos)
        self.hitbox.set_rotation(self.angle)

    def take_damage(self, dmg: int) -> int:
        prev_hp = self.hp
        self.hp -= dmg
        return prev_hp - self.hp

    def draw(self, target: pygame.Surface) -> None:
        target.blit(self.image, self.screen_pos - Vec(self.image.get_rect().size) / 2)

    def get_nearby_entities(self) -> list[Entity]:
        cx, cy = self.scene.spacial_hash_key(self.pos)
        nearby: list[Entity] = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nearby.extend(self.scene.collideable_buckets.get(Vec(cx+dx, cy+dy), {}).get("entity", []))
        return nearby

    def colliding_entities(self) -> list[Entity]:
        entities = []
        # # the player
        # if self != self.scene.player \
        #    and self.scene.player.pos.distance_to(self.pos) < self.size.magnitude() + self.scene.player.size.magnitude() \
        #    and self.hitbox.is_colliding(self.scene.player.hitbox):
        #     entities.append(self.scene.player)

        self_rad = (self.size.x + self.size.y) / 2

        def is_close(other: Entity) -> bool:
            other_rad = (other.size.x + other.size.y) / 2
            return other.pos.distance_squared_to(self.pos) < (self_rad + other_rad) ** 2

        # enemies
        for entity in self.get_nearby_entities():
            if self != entity and is_close(entity) and self.hitbox.is_colliding(entity.hitbox):
                entities.append(entity)

        return entities
