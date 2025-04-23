from __future__ import annotations

from pygame import Surface
from src.core import *
from .spell import Spell

class Gust(Spell):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, 0, "air")
        self.angle: float
        self.hitbox = Hitbox(self.pos, [])
        self.hitbox.set_size_rect(160, 380)
        self.size = Vec(160, 380)
        self.hitbox.translate(Vec(0, -190))
        self.anim_timer = Timer(0.3)

    def draw_charge(self, screen: Surface) -> None:
        pass
    def update_charge(self, dt: float) -> None:
        pass

    def update_aiming(self, dt: float) -> None:
        self.pos = self.scene.player.pos
        self.hitbox.set_rotation(self.angle + pi / 2, False)
        self.hitbox.set_position(self.pos)

    def update_spell(self, dt: float) -> None:
        pass

    def draw_aiming(self, screen: Surface) -> None:
        mpos = self.game.mouse_pos
        player = self.scene.player
        self.angle = atan2((mpos.y - player.screen_pos.y), (mpos.x - player.screen_pos.x))
        flipped_angle = self.angle + pi
        pygame.draw.line(screen, (120, 120, 120), player.screen_pos, player.screen_pos + 50 * Vec(cos(flipped_angle), sin(flipped_angle)), 5)
        rotangle = 270 - 180 / pi * self.angle
        origimg = pygame.surface.Surface((160, 380), pygame.SRCALPHA)
        origimg.set_colorkey((0, 0, 0))
        pygame.draw.rect(origimg, (120, 120, 120, 100), origimg.get_rect())
        rotimg = pygame.transform.rotate(origimg, rotangle)
        screen.blit(rotimg, player.screen_pos + 190 * Vec(cos(self.angle), sin(self.angle)) - Vec(rotimg.size) / 2)
        # hitbox debugging
        if Debug.on():
            pygame.draw.polygon(screen, (255, 0, 0), [Vec(p) - self.scene.player.pos + self.scene.player.screen_pos for p in self.hitbox.get_hitbox()], 2)

    def draw_spell(self, screen: Surface) -> None:
        player = self.scene.player
        screen_pos = player.screen_pos + 690 * self.anim_timer.progress * Vec(
                                   cos(self.angle), sin(self.angle)) + (
                                   uniform(-50, 50), uniform(-50, 50))
        pygame.draw.circle(screen, AIR, screen_pos, 10)
        if self.anim_timer.done:
            self.kill()

    def trigger_spell(self) -> None:
        super().trigger_spell()
        for projectile in self.scene.projectiles:
            if projectile.element != "air" and projectile.pos.distance_to(self.pos) < projectile.rad + self.size.magnitude() \
            and self.hitbox.is_colliding(projectile.hitbox):
                change = Vec(cos(self.angle), sin(self.angle)) * (400 * 10 / projectile.rad)
                projectile.external_acc += change
        self.scene.player.ext_acc = -2000 * Vec(cos(self.angle), sin(self.angle))
        self.anim_timer.reset()
