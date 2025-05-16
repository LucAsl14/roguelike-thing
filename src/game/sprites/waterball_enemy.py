from __future__ import annotations
from src.core import *
from .enemy import Enemy
from .waterball import Waterball

class WaterballEnemy(Enemy):
    def __init__(self, scene: MainScene, pos: Vec) -> None:
        super().__init__(scene, 10, pos)
        self.shooting_cooldown = Timer(5)
        tint = pygame.Surface(self.image.get_size()).convert_alpha()
        tint.fill((0, 0, 200))
        self.image.blit(tint, (0, 0), special_flags=BLEND_RGBA_MULT)

    def update_movement(self, dt: float) -> None:
        dist = self.get_player_distance()
        if dist > 400:
            self.acc = 400 * Vec(1, 0).rotate(degrees(self.get_player_direction()))
        elif dist < 300:
            self.acc = 400 * Vec(-1, 0).rotate(degrees(self.get_player_direction()))
        else:
            self.acc = 400 * Vec(0, 1).rotate(degrees(self.get_player_direction()))

    def update_attack(self, dt: float) -> None:
        if self.get_player_distance() > 100 and self.shooting_cooldown.done:
            waterball = Waterball(self.scene, Vec(1, 0).rotate(degrees(self.get_player_direction())), "enemy")
            self.scene.add(waterball)
            waterball.pos = self.pos.copy()
            self.shooting_cooldown.reset()
