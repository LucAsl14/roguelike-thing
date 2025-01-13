from __future__ import annotations
from src.core import *
from .projectile import Projectile
from pygame import Surface
from .construct import Construct

class Waterball(Projectile):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, 5, 400, 1.5, 10, "water")
        self.exploding = False
        self.exploding_timer = Timer(0.1)
        self.size = 20

    def draw_charge(self, screen: Surface) -> None:
        if self.pos.distance_to(self.scene.player.pos) > 800:
            return
        screen_pos = Vec(self.pos.x - self.scene.player.pos.x, self.scene.player.pos.y - self.pos.y)
        screen_pos += (screen.width / 2, screen.height / 2)
        pygame.draw.circle(screen, (50, 100, 200), screen_pos, self.charging_time.elapsed * self.size / 1.5)

    def update_spell(self, dt: float) -> None:
        super().update_spell(dt)
        if self.exploding:
            self.size = 20 + 180 * self.exploding_timer.elapsed / self.exploding_timer.duration
            if self.exploding_timer.done:
                # testing an exploding mechanic
                self.rect = pygame.Rect(self.pos - (200, 200), (400, 400))
                for construct in self.scene.constructs:
                    if self.rect.colliderect(construct.rect):
                        construct.take_damage(10)
                for projectile in self.scene.projectiles:
                    if self.rect.colliderect(projectile.rect) and projectile.element != self.element:
                        projectile.take_damage(10)
                super().kill()


    def draw_spell(self, screen: Surface) -> None:
        if self.pos.distance_to(self.scene.player.pos) > 800:
            return
        screen_pos = Vec(self.pos.x - self.scene.player.pos.x, self.scene.player.pos.y - self.pos.y)
        screen_pos += (screen.width / 2, screen.height / 2)
        pygame.draw.circle(screen, (50, 100, 200), screen_pos, self.size)
        self.rect = pygame.Rect(self.pos - (self.size / 2, self.size / 2), (self.size, self.size))

    def collide(self, target: Construct | Projectile) -> None:
        # deals double damage against fire (testing this out)
        if target.element == "fire":
            self.damage *= 2
        super().collide(target)
        if target.element == "fire":
            self.damage //= 2

    def kill(self) -> None:
        if not self.exploding:
            self.exploding_timer.reset()
        self.exploding = True
        self.vel = Vec()
