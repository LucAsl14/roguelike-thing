from __future__ import annotations

from pygame import Surface
from src.core import *
from .construct import Construct

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .entity import Entity
class Rollout(Construct):
    def __init__(self, scene: MainScene, target_posdiff: Vec) -> None:
        super().__init__(scene, 2, 4, 20)
        self.copy_timer = LoopTimer(0.2, -1)
        self.copies_made = 0
        self.target_posdiff = target_posdiff
        self.angle: float = 0
        self.pos = Vec()
        self.offset = Vec()
        self.size: Vec
        self.is_original = True

        self.target_angle = atan2(target_posdiff.y, target_posdiff.x)

        self.hitbox = Hitbox(self.pos, [])
        self.hitbox.set_size_rect(10, 30)

    def draw_charge(self, screen: Surface) -> None:
        # pygame.draw.line(screen, (120, 120, 120), self.scene.player.screen_pos, self.game.mouse_pos, 3)
        # more rectangle rotating
        origimg = pygame.surface.Surface((30, 10))
        origimg.set_colorkey((0, 0, 0))
        pygame.draw.rect(origimg, EARTH, origimg.get_rect())
        rotimg = pygame.transform.rotate(origimg, 90 - degrees(self.angle))
        self.size = Vec(rotimg.get_rect().size)
        screen.blit(rotimg, self.screen_pos - self.size / 2)

    def update_charge(self, dt: float) -> None:
        # previously used to allow you to change directions while aiming...
        # mousediff = self.game.mouse_pos - self.scene.player.screen_pos
        # self.target_angle = atan2(mousediff.y, mousediff.x)
        if self.copy_timer.done and self.copies_made < 5:
            spell = Rollout(self.scene, self.target_posdiff)
            self.scene.add(spell)
            self.copies_made += 1
            spell.angle = self.angle + pi/3 * (self.copies_made)
            spell.is_original = False
            spell.trigger_spell()
            spell.copy_timer.pause()
            spell.charging_time = self.charging_time
        self.offset -= self.offset.normalize() * dt * 320
        if self.offset.magnitude() < 50:
            self.offset = 50 * Vec(cos(self.angle), sin(self.angle))
        self.pos = self.scene.player.pos + self.offset
        # locks the player's movement
        self.scene.player.vel = Vec()
        self.hitbox.set_position(self.pos)
        self.hitbox.set_rotation(self.angle)


    def draw_spell(self, screen: Surface) -> None:
        # even more rectangle rotating
        origimg = pygame.surface.Surface((30, 10))
        origimg.set_colorkey((0, 0, 0))
        pygame.draw.rect(origimg, EARTH, origimg.get_rect())
        rotimg = pygame.transform.rotate(origimg, 90 - degrees(self.angle))
        self.size = Vec(rotimg.get_rect().size)
        screen.blit(rotimg, self.screen_pos - self.size / 2)
        # hitbox debugging
        if Debug.on():
            pygame.draw.polygon(screen, (255, 0, 0), [Vec(p) - self.scene.player.pos + self.scene.player.screen_pos for p in self.hitbox.get_hitbox()], 2)

    def update_spell(self, dt: float) -> None:
        self.angle += 2
        blocked = False
        for construct in self.scene.constructs:
            if self.scene.player in construct.colliding_entities():
                blocked = True
        if not blocked:
            self.scene.player.vel = 1050 * Vec(cos(self.target_angle), sin(self.target_angle))
        self.offset = 50 * Vec(cos(self.angle), sin(self.angle))
        self.pos = self.scene.player.pos + self.offset
        self.hitbox.set_position(self.pos)
        self.hitbox.set_rotation(self.angle, False)
        super().update_spell(dt)

    def trigger_spell(self) -> None:
        self.copy_timer.reset()
        super().trigger_spell()
        self.offset = 320 * Vec(cos(self.angle), sin(self.angle))
        self.pos = self.scene.player.pos + self.offset

    def collide(self, entities: list[Entity]) -> None:
        for entity in entities:
            entity.vel = 100 * 10 * Vec((entity.pos - self.pos)).normalize()
