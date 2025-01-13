from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell

class Gust(Spell):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, 0, "air")
        self.angle: float
        self.rect = pygame.Rect()
        self.anim_timer = Timer(0.1)

    def draw_charge(self, screen: Surface) -> None:
        pass
    def update_charge(self, dt: float) -> None:
        pass
    def update_aiming(self, dt: float) -> None:
        pass
    def update_spell(self, dt: float) -> None:
        pass

    def draw_aiming(self, screen: Surface) -> None:
        mpos = self.game.mouse_pos
        player = self.scene.player
        self.angle = atan2((player.screen_pos.y - mpos.y), (player.screen_pos.x - mpos.x))
        pygame.draw.line(screen, (120, 120, 120), player.screen_pos, player.screen_pos + (50 * cos(self.angle), 50 * sin(self.angle)), 5)
        rotangle = 270 - 180 / pi * self.angle
        self.angle -= pi
        origimg = pygame.surface.Surface((160, 380), pygame.SRCALPHA)
        origimg.set_colorkey((0, 0, 0))
        pygame.draw.rect(origimg, (120, 120, 120, 100), origimg.get_rect())
        rotimg = pygame.transform.rotate(origimg, rotangle)
        self.rect = pygame.Rect(player.pos + (190 * cos(self.angle), 190 * sin(self.angle)) - (rotimg.size[0] / 2, rotimg.size[1] / 2), rotimg.get_rect().size)
        screen.blit(rotimg, player.screen_pos + (190 * cos(self.angle), 190 * sin(self.angle)) - (rotimg.size[0] / 2, rotimg.size[1] / 2))
        self.angle += pi

    def draw_spell(self, screen: Surface) -> None:
        player = self.scene.player
        pos = player.screen_pos - (190 * self.anim_timer.progress * cos(self.angle),
                                   190 * self.anim_timer.progress * sin(self.angle)) + (
                                   uniform(-50, 50), uniform(-50, 50))
        pygame.draw.circle(screen, (200, 200, 200), pos, 10)

    def trigger_spell(self) -> None:
        super().trigger_spell()
        for projectile in self.scene.projectiles:
            if projectile.rect.colliderect(self.rect):
                projectile.vel += (-400 * cos(self.angle), 400 * sin(self.angle))
        self.scene.player.vel += (2000 * cos(self.angle), -2000 * sin(self.angle))
        self.anim_timer.reset()
