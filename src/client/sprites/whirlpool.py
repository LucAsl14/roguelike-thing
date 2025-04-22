from __future__ import annotations

from pygame import Surface
from client.core import *
from .area_spell import AreaSpell

class Whirlpool(AreaSpell):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, 1, "air", 15, 145, "GROUND")
        self.circle_offsets: list[Vec] = []
        self.new_circle_timer = LoopTimer(0.1)

    def draw_charge(self, screen: Surface) -> None:
        trans_surf = pygame.surface.Surface(Vec(2 * self.rad), pygame.SRCALPHA)
        pygame.draw.circle(trans_surf, WATER, Vec(self.rad), self.rad)
        trans_surf.set_alpha(int(255 * self.charging_time.progress))
        screen.blit(trans_surf, self.screen_pos - Vec(self.rad))

    def draw_spell(self, screen: Surface) -> None:
        pygame.draw.circle(screen, WATER, self.screen_pos, self.rad)
        trans_surf = pygame.surface.Surface(Vec(2 * self.rad), pygame.SRCALPHA)
        for circle in self.circle_offsets:
            pygame.draw.circle(trans_surf, (220, 220, 220, 200), Vec(self.rad) + circle, 10)
        screen.blit(trans_surf, self.screen_pos - Vec(self.rad))

    def update_spell(self, dt: float) -> None:
        player = self.scene.player
        if dist := player.pos.distance_to(self.pos) < self.rad:
            player.vel *= ((1 - dist / self.rad) / 4) ** dt
            player.vel += (1 - dist / self.rad) * (self.pos - player.pos).normalize() * 2000 * dt
            player.vel += (1.1 - dist / self.rad) * (self.pos - player.pos).normalize().rotate(90) * 1500 * dt
        for projectile in self.scene.projectiles:
            if dist := projectile.pos.distance_to(self.pos) < self.rad:
                projectile.vel *= ((1 - dist / self.rad) / 4) ** dt
                projectile.vel += (1 - dist / self.rad) * (self.pos - projectile.pos).normalize() * 2000 * dt
                projectile.vel += (1.1 - dist / self.rad) * (self.pos - projectile.pos).normalize().rotate(90) * 1500 * dt

        # art part
        for i in range(len(self.circle_offsets)):
            circle = self.circle_offsets[i]
            dist = Vec(circle).distance_to((0, 0))
            circle = circle + (dist / self.rad) * (-circle).normalize() * 90 * dt
            circle = circle + (circle).normalize().rotate(-90) * 240 * dt
            self.circle_offsets[i] = circle
        if self.new_circle_timer.done:
            self.circle_offsets.append(self.random_circle_point())
        super().update_spell(dt)

    def random_circle_point(self) -> Vec:
        angle = uniform(0, 2*pi)
        scalar = self.rad
        return scalar * Vec(cos(angle), sin(angle))

    def trigger_spell(self) -> None:
        for _ in range(10):
            self.circle_offsets.append(self.random_circle_point())
        super().trigger_spell()
