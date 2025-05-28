from __future__ import annotations

from pygame import Surface
from src.core import *
from .construct import Construct
from random import uniform
class EarthBlock(Construct):
    def __init__(self, scene: MainScene, target_posdiff: Vec, origin: str, size: Vec, angle: float) -> None:
        super().__init__(scene, 0.2, 15, 20)
        # testing some graphic changing depending on damage
        self.extra_damaged = False
        self.hitbox = Hitbox(self.pos, [])
        self.hitbox.set_size_rect(size.x, size.y)
        self.angle = angle
        self.pos = self.scene.player.pos + target_posdiff
        self.original_size = size

    def draw_charge(self, screen: Surface) -> None:
        self.draw_spell(screen)
        for _ in range(5):
            dpos = Vec(cos(uniform(0, 360)), sin(uniform(0, 360)))
            dpos *= 100 * (1 - self.charging_time.progress)
            if (self.pos + dpos).distance_to(self.scene.player.pos) > 800:
                continue
            pygame.draw.circle(screen, EARTH, self.screen_pos + dpos, 10)

    def draw_spell(self, screen: Surface) -> None:
        # more rectangle rotating
        origimg = pygame.surface.Surface(self.original_size)
        origimg.set_colorkey((0, 0, 0))
        pygame.draw.rect(origimg, EARTH, origimg.get_rect())
        if self.extra_damaged:
            pygame.draw.line(origimg, (40, 20, 10), (10, 0), (40, 40))
            pygame.draw.line(origimg, (40, 20, 10), (30, 0), (10, 40))
        rotimg = pygame.transform.rotate(origimg, self.angle)
        if self.size == Vec(): # init size for the first time
            self.size = Vec(rotimg.get_rect().size)
        screen.blit(rotimg, self.screen_pos - self.size / 2)
        # hitbox debugging
        if Debug.on():
            pygame.draw.polygon(screen, (255, 0, 0), [Vec(p) - self.scene.player.pos + self.scene.player.screen_pos for p in self.hitbox.get_hitbox()], 2)

    def trigger_spell(self) -> None:
        self.hitbox.set_rotation(self.angle)
        self.hitbox.set_position(self.pos)

    def take_damage(self, dmg: int) -> int:
        dmg_taken = super().take_damage(dmg)
        if self.hp <= 10:
            self.extra_damaged = True
        return dmg_taken
