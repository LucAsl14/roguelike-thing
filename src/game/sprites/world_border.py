from __future__ import annotations
from src.core import *

class WorldBorder(Sprite):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, "SKY")

        self.pos = Vec(0)
        self.rad = 10000

        self.scene = scene
        self.old_pos = self.pos
        self.target_pos = self.pos
        self.old_rad = self.rad
        self.target_rad = self.rad
        self.move_timer = Timer(1e-6) # a 0-length temp timer
        self.rgba: List[int] = [0, 0, 0, 0]

    def update(self, dt: float) -> None:
        distance_from_border = (int(self.scene.player.pos.distance_to(self.pos)) - self.rad)
        self.rgba[0] = int(170 + max(0, min(85, (distance_from_border - 500) // 7)))    # from 170 to 255 (500 to 1000)
        self.rgba[1] = int( 50 - max(0, min(50, (distance_from_border - 500) // 10)))   # 50 to 0 (500 to 1000)
        self.rgba[2] = int(240 - max(0, min(240, (distance_from_border - 500) // 4)))   # 240 to 0 (500 to 1000)
        self.rgba[3] = int(155 + max(0, min(50, distance_from_border // 10)))           # from 155 to 205 (0 to 500)

        self.pos = self.old_pos + self.move_timer.progress * (self.target_pos - self.old_pos)
        self.rad = self.old_rad + self.move_timer.progress * (self.target_rad - self.old_rad)


    def draw(self, target: pygame.Surface) -> None:
        purple_overlay = pygame.surface.Surface(target.size, pygame.SRCALPHA)
        purple_overlay.fill(self.rgba)
        pygame.draw.circle(purple_overlay, (0, 0, 0, 0), self.screen_pos, self.rad)
        target.blit(purple_overlay, (0, 0))

    def move_to(self, target_pos: Vec | None, target_rad: float | None, time: float) -> None:
        self.old_pos = self.pos
        self.old_rad = self.rad
        if target_pos == None:  self.target_pos = self.pos
        else:                   self.target_pos = target_pos
        if target_rad == None:  self.target_rad = self.rad
        else:                   self.target_rad = target_rad
        self.move_timer.reset(time)
