from __future__ import annotations
from src.core import *
from typing import List

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
        self.moving_timer = Timer(0)
        self.scheduling_timer = Timer(0)
        self.rgba: List[int] = [0, 0, 0, 0]
        self.moving = False
        self.scheduling = False

    def update(self, dt: float) -> None:
        distance_from_border = (int(self.scene.player.pos.distance_to(self.pos)) - self.rad)
        self.rgba[0] = int(170 + max(0, min(85, (distance_from_border - 500) // 7)))    # from 170 to 255 (500 to 1000)
        self.rgba[1] = int( 50 - max(0, min(50, (distance_from_border - 500) // 10)))   # 50 to 0 (500 to 1000)
        self.rgba[2] = int(240 - max(0, min(240, (distance_from_border - 500) // 4)))   # 240 to 0 (500 to 1000)
        self.rgba[3] = int(155 + max(0, min(50, distance_from_border // 10)))           # from 155 to 205 (0 to 500)

        if self.scheduling and self.scheduling_timer.done:
            self.scheduling = False
            self.moving = True
            self.moving_timer.resume()
        if self.moving:
            self.pos = self.old_pos + self.moving_timer.progress * (self.target_pos - self.old_pos)
            self.rad = self.old_rad + self.moving_timer.progress * (self.target_rad - self.old_rad)
            if self.moving_timer.done:
                self.moving = False


    def draw(self, target: pygame.Surface) -> None:
        purple_overlay = pygame.surface.Surface(target.size, pygame.SRCALPHA)
        purple_overlay.fill(self.rgba)
        pygame.draw.circle(purple_overlay, (0, 0, 0, 0), self.screen_pos, self.rad)
        if self.scheduling or self.moving:
            pygame.draw.circle(purple_overlay, (255, 255, 255, 200), self.target_pos - self.scene.camera.pos, self.target_rad, 3)
        if self.scene.player.pos.distance_to(self.target_pos) > self.target_rad:
            center = self.target_pos - self.scene.camera.pos
            player_point = self.scene.player.screen_pos
            pygame.draw.line(purple_overlay, (255, 255, 255, 200), player_point, center - (center - player_point).normalize() * self.target_rad)
        target.blit(purple_overlay, (0, 0))

    def schedule_move_to(self, target_pos: Vec | None, target_rad: float | None, move_time: float, wait_time: float) -> None:
        self.old_pos = self.pos
        self.old_rad = self.rad
        if target_pos == None:  self.target_pos = self.pos
        else:                   self.target_pos = target_pos
        if target_rad == None:  self.target_rad = self.rad
        else:                   self.target_rad = target_rad
        self.moving_timer.reset(move_time)
        self.moving_timer.pause()
        self.scheduling_timer.reset(wait_time)
        self.scheduling = True
        self.moving = False
