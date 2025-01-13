from __future__ import annotations

from pygame import Surface
from src.core import *
from .construct import Construct
from random import uniform

class EarthBlock(Construct):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, 0.2, 15, 20)
        self.angle: float
        # testing some graphic changing depending on damage
        self.extra_damaged = False

    def draw_aiming(self, screen: Surface) -> None:
        # all of this code just to rotate a rectangle?????
        mpos = self.game.mouse_pos
        player = self.scene.player
        self.angle = 90 - 180 / pi * atan2((player.screen_pos.y - mpos.y), (player.screen_pos.x - mpos.x))
        origimg = pygame.surface.Surface((50, 40))
        origimg.set_colorkey((0, 0, 0))
        pygame.draw.rect(origimg, (120, 120, 120), origimg.get_rect())
        rotimg = pygame.transform.rotate(origimg, self.angle)
        screen.blit(rotimg, mpos - (rotimg.size[0] / 2, rotimg.size[1] / 2))

    def draw_charge(self, screen: Surface) -> None:
        self.draw_spell(screen)
        for _ in range(5):
            dpos = Vec(cos(uniform(0, 360)) * 100 * (1 - self.charging_time.progress),
                       sin(uniform(0, 360)) * 100 * (1 - self.charging_time.progress))
            if (self.pos + dpos).distance_to(self.scene.player.pos) > 800:
                continue
            pygame.draw.circle(screen, (100, 60, 30), self.screen_pos + (dpos.x, -dpos.y), 10)

    def draw_spell(self, screen: Surface) -> None:
        posdiff = self.pos - self.scene.player.pos
        # hitbox????/
        self.rect = pygame.Rect(self.pos - (25, 25), (50, 50))
        self.screen_pos = self.scene.player.screen_pos + (posdiff.x, -posdiff.y)
        if self.pos.distance_to(self.scene.player.pos) > 800:
            return
        # more rectangle rotating
        origimg = pygame.surface.Surface((50, 40))
        origimg.set_colorkey((0, 0, 0))
        pygame.draw.rect(origimg, (100, 60, 30), origimg.get_rect())
        if self.extra_damaged:
            pygame.draw.line(origimg, (40, 20, 10), (10, 0), (40, 40))
            pygame.draw.line(origimg, (40, 20, 10), (30, 0), (10, 40))
        rotimg = pygame.transform.rotate(origimg, self.angle)
        screen.blit(rotimg, self.screen_pos - (rotimg.size[0] / 2, rotimg.size[1] / 2))

    def trigger_spell(self) -> None:
        super().trigger_spell()

    def take_damage(self, dmg: int) -> int:
        dmg_taken = super().take_damage(dmg)
        if self.hp <= 10:
            self.extra_damaged = True
        return dmg_taken
