from __future__ import annotations

from pygame import Surface
from src.core import *
from .construct import Construct

class Rollout(Construct):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, 2, 4, 20)
        self.copy_timer = LoopTimer(0.2, -1)
        self.copies_made = 0
        self.angle: float = 0
        self.target_angle: float
        self.pos = Vec()
        self.offset = Vec()
        self.size: Vec
        # testing some graphic changing depending on damage
        self.extra_damaged = False

    def draw_aiming(self, screen: Surface) -> None:
        pygame.draw.line(screen, (120, 120, 120), self.scene.player.screen_pos, self.game.mouse_pos, 3)

    def draw_charge(self, screen: Surface) -> None:
        pygame.draw.line(screen, (120, 120, 120), self.scene.player.screen_pos, self.game.mouse_pos, 3)
        # pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.rect.topleft + self.scene.player.screen_pos - self.scene.player.pos, self.rect.size))
        # more rectangle rotating
        origimg = pygame.surface.Surface((30, 10))
        origimg.set_colorkey((0, 0, 0))
        pygame.draw.rect(origimg, EARTH, origimg.get_rect())
        if self.extra_damaged:
            pygame.draw.line(origimg, (40, 20, 10), (3, 0), (18, 6))
            pygame.draw.line(origimg, (40, 20, 10), (5, 0), (5, 10))
        rotimg = pygame.transform.rotate(origimg, 90 - degrees(self.angle))
        self.size = Vec(rotimg.get_rect().size)
        screen.blit(rotimg, self.screen_pos - self.size / 2)
        self.rect = pygame.Rect(self.pos - Vec(self.size) / 2, self.size)

    def update_charge(self, dt: float) -> None:
        mousediff = self.game.mouse_pos - self.scene.player.screen_pos
        self.target_angle = atan2(mousediff.y, mousediff.x)
        if self.copy_timer.done and self.copies_made < 5:
            spell = Rollout(self.scene)
            self.scene.add(spell)
            self.copies_made += 1
            spell.angle = self.angle + pi/3 * (self.copies_made)
            spell.aiming = False
            spell.trigger_spell()
            spell.copy_timer.pause()
            spell.charging_time = self.charging_time
        self.offset -= self.offset.normalize() * dt * 320
        if self.offset.magnitude() < 50:
            self.offset = 50 * Vec(cos(self.angle), sin(self.angle))
        self.pos = self.scene.player.pos + self.offset
        self.scene.player.vel = Vec()


    def draw_spell(self, screen: Surface) -> None:
        # pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.rect.topleft + self.scene.player.screen_pos - self.scene.player.pos, self.rect.size))
        # even more rectangle rotating
        origimg = pygame.surface.Surface((30, 10))
        origimg.set_colorkey((0, 0, 0))
        pygame.draw.rect(origimg, EARTH, origimg.get_rect())
        if self.extra_damaged:
            pygame.draw.line(origimg, (40, 20, 10), (3, 0), (18, 6))
            pygame.draw.line(origimg, (40, 20, 10), (5, 0), (5, 10))
        rotimg = pygame.transform.rotate(origimg, 90 - degrees(self.angle))
        self.size = Vec(rotimg.get_rect().size)
        screen.blit(rotimg, self.screen_pos - self.size / 2)
        self.rect = pygame.Rect(self.pos - Vec(self.size) / 2, self.size)

    def update_spell(self, dt: float) -> None:
        self.angle += radians(2)
        self.scene.player.vel = 1050 * Vec(cos(self.target_angle), sin(self.target_angle))
        self.offset = 50 * Vec(cos(self.angle), sin(self.angle))
        self.pos = self.scene.player.pos + self.offset
        super().update_spell(dt)

    def trigger_spell(self) -> None:
        self.copy_timer.reset()
        super().trigger_spell()
        self.offset = 320 * Vec(cos(self.angle), sin(self.angle))
        self.pos = self.scene.player.pos + self.offset
