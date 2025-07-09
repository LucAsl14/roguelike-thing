from __future__ import annotations
from src.core import *
from typing import Generator

# TODO + NOTE: Collision performance is temporarily slightly worse PROBABLY due
# to a lack of distinct buckets for different entity types. This will be
# implemented later in a more sophisticated way that can be expanded to any
# number of entity types.

class Entity(Sprite):
    def __init__(self, scene: MainScene, layer: str, hitbox: Hitbox, hp: int) -> None:
        super().__init__(scene, layer)
        self.scene = scene

        # combat
        self.hp = hp

        # movement-related variables
        self.pos = hitbox.center.copy()
        self.prev_pos = self.pos.copy()
        self.prev_hash = self.scene.spacial_hash_key(self.pos)
        self.scene.entity_buckets[self.prev_hash].append(self)
        self.vel = Vec()
        self.acc = Vec()

        # physical properties
        self.hitbox = hitbox
        self.size = hitbox.size.copy()
        self.angle = 0

        self.no_collision = False  # if True, the entity will not collide with others
        self.collision_ignore_entities: set[Entity] = set() # entities to ignore collisions with
        # NOTE: This will be removed in favor of a default-ignore system that would be more performant
        # See note at the top of this file
        self.collision_ignore_classes: tuple[type[Entity], ...] = tuple() # classes of entities to ignore collisions with
        self.soft_collision = 0.0  # percentage of collision response to reduce

    def update_position(self, dt: float) -> None:
        # All of vel, acc, ext_vel, etc. are measured in unit/s
        for entity in self.get_colliding_entities():
            collision_force = Vec((entity.pos - self.pos)).normalize() * 6000
            self.apply_impulse(collision_force * (1 - entity.soft_collision))

        self.vel += self.acc * dt
        self.pos += self.vel * dt
        self.hitbox.set_position(self.pos)
        self.hitbox.set_rotation(self.angle)
        hash = self.scene.spacial_hash_key(self.pos)
        if hash != self.prev_hash:
            self.scene.entity_buckets[self.prev_hash].remove(self)
            self.scene.entity_buckets[hash].append(self)

        self.acc = Vec()
        self.prev_pos = self.pos.copy()
        self.prev_hash = hash

    def apply_force(self, force: Vec) -> None:
        self.acc += force

    def apply_impulse(self, impulse: Vec) -> None:
        self.acc += impulse / self.game.dt

    def take_damage(self, dmg: int) -> int:
        # TODO: add argument that specifies source of damage and allow for selective damage immunity
        prev_hp = self.hp
        self.hp -= dmg
        return prev_hp - self.hp

    def draw_centered(self, target: pygame.Surface, surface: pygame.Surface) -> None:
        target.blit(surface, self.screen_pos - Vec(surface.get_rect().size) / 2)

    def get_nearby_entities(self) -> Generator[Entity, None, None]:
        cx, cy = self.scene.spacial_hash_key(self.pos)
        for dx, dy in iter_rect(-1, 1, -1, 1):
            yield from self.scene.entity_buckets.get(Vec(cx + dx, cy + dy), [])

    def get_colliding_entities(self) -> Generator[Entity, None, None]:
        # # the player
        # if self != self.scene.player \
        #    and self.scene.player.pos.distance_to(self.pos) < self.size.magnitude() + self.scene.player.size.magnitude() \
        #    and self.hitbox.is_colliding(self.scene.player.hitbox):
        #     yield self.scene.player
        if self.no_collision: return

        # enemies
        for entity in self.get_nearby_entities():
            if isinstance(entity, self.collision_ignore_classes): continue
            if entity in self.collision_ignore_entities: continue
            if self is entity: continue
            if self.hitbox.is_colliding(entity.hitbox):
                yield entity

    def set_collision_ignore_entities(self, *entities: Entity) -> None:
        """Set the entity to ignore collisions with a specific entity."""
        self.collision_ignore_entities = set(entities)

    def set_collision_ignore_classes(self, *classes: type[Entity]) -> None:
        """Set the entity to ignore collisions with all entities of a specific class."""
        self.collision_ignore_classes = classes

    def set_no_collision(self, yes: bool) -> None:
        """Set whether the entity should not collide with others. (default: False)

        Setting this to True will skip all collision checks for this entity."""
        self.no_collision = yes

    def set_soft_collision(self, percentage: float) -> None:
        """Set the entity's soft collision percentage. (default: 0.0)

        This will reduce the collision response by the specified percentage.

        ex.
        - set_soft_collision(0.5) will reduce the collision response by 50%.
        - set_soft_collision(1.0) will disable the collision response entirely
        (note that this is different from `set_no_collision` as it still
        processes collisions, but does not apply any collision response).
        - set_soft_collision(0.0) will enable the full collision response"""
        self.soft_collision = percentage
