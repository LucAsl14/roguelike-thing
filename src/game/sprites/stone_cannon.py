from __future__ import annotations

from pygame import Surface
from .construct import Construct
from src.core import *
from .projectile import Projectile

class StoneCannon(Projectile):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, 10, 300, 0, 5, "earth", 8)
        self.iframe = Timer(0.75)
        self.angle = 0
        self.turn_speed = 5
        self.target_pos = Vec()

    def draw_charge(self, screen: Surface) -> None:
        pass
    def update_charge(self, dt: float) -> None:
        pass

    def draw_spell(self, screen: Surface) -> None:
        if self.pos.distance_to(self.scene.player.pos) > 800:
            return
        self.set_screen_pos(screen)
        pygame.draw.circle(screen, (100, 60, 30), self.screen_pos, self.rad)
        pygame.draw.circle(screen, (100, 60, 30), self.screen_pos + (8 * cos(self.angle), 8 * sin(self.angle)), self.rad / 2)

    def update_spell(self, dt: float) -> None:
        self.vel = Vec(self.speed * cos(self.angle), -self.speed * sin(self.angle))
        # custom external acc handling
        self.vel += self.external_acc
        if self.external_acc.magnitude() > 0:
            self.angle = atan2(self.vel.y, self.vel.x)
            self.speed = self.vel.magnitude()
        self.external_acc = Vec()
        posdiff = self.target_pos - self.pos
        target_angle = atan2(-posdiff.y, posdiff.x)
        degdiff = ((((self.angle - target_angle) * 180 / pi) % 360) + 360) % 360
        if degdiff <= 2 or degdiff >= 358:
            self.turn_speed = 0
            self.speed = 1000 # 1000
        elif degdiff < 180:
            self.angle -= self.turn_speed * dt
        else:
            self.angle += self.turn_speed * dt
        super().update_spell(dt)

    def trigger_spell(self) -> None:
        if self.aiming:
            for _ in range(4):
                spell = StoneCannon(self.scene)
                self.scene.add(spell)
                spell.aiming = False
                spell.trigger_spell()
                spell.speed += int(uniform(-200, 201))
        super().trigger_spell()
        player = self.scene.player
        screen_pos_diff = (self.game.mouse_pos - player.screen_pos)
        screen_pos_diff.y *= -1
        self.target_pos = screen_pos_diff + (player.pos.x , player.pos.y)
        posdiff = self.target_pos - self.pos
        target_angle = atan2(-posdiff.y, posdiff.x)
        self.angle = uniform(target_angle + pi/2 + pi/4, target_angle + 3*pi/2 - pi/4)

    def collide(self, target: Construct | Projectile) -> None:
        if isinstance(target, StoneCannon):
            return
        super().collide(target)
