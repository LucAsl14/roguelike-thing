from __future__ import annotations
from src.core import *
import numpy as np

class TerrainBackground(Sprite):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, "BACKGROUND")
        self.scene = scene
        self.BLEND_DISTANCE = 50
        self.SCALE_FACTOR = 4
        self.background = (120, 160, 80)
        # temporary color points
        self.color_circles = [
            # pos, rad, color
            # (Vec(50, 50), 100, (153, 68, 78)),
            # (Vec(-50, -50), 100, (138, 100, 219))
            (Vec(-100, 0), 150, (255, 0, 0)),
            (Vec(50, -86.6), 150, (0, 255, 0)),
            (Vec(50, 86.6), 150, (0, 0, 255)),
        ]

    def update(self, dt: float) -> None:
        pass
        # self.pos = self.scene.player.pos
        # r = g = b = weight = total_weight = 0

        # for pos, rad, color in self.color_circles:
        #     dist = self.pos.distance_to(pos)
        #     if dist <= rad:
        #         weight = 1
        #     elif dist - rad < self.BLEND_DISTANCE:
        #         weight = 1 - ((dist - rad) / self.BLEND_DISTANCE) ** 2
        #     else:
        #         weight = 0

        #     total_weight += weight
        #     r += color[0] * weight
        #     g += color[1] * weight
        #     b += color[2] * weight

        # if total_weight < 1:
        #     bg_weight = 1 - total_weight
        #     r += self.background[0] * bg_weight
        #     g += self.background[1] * bg_weight
        #     b += self.background[2] * bg_weight
        #     total_weight = 1

        # final_color = (
        #     int(r / total_weight),
        #     int(g / total_weight),
        #     int(b / total_weight)
        # )
        # self.color = final_color

    def draw(self, target: pygame.Surface) -> None:
        self.pos = self.scene.camera.pos

        small_size = (960 / self.SCALE_FACTOR, 540 / self.SCALE_FACTOR)
        terrain_background = pygame.surface.Surface(small_size, pygame.SRCALPHA)
        self.draw_mixed_background(terrain_background)
        # terrain_background.fill(self.background)
        # terrain_background.fill(self.color)
        # for circle in self.color_circles:
        #     soft_c = pygame.surface.Surface(target.size, pygame.SRCALPHA)
        #     self.draw_soft_circle(soft_c, *circle)
        #     terrain_background.blit(soft_c, special_flags=pygame.BLEND_RGBA_ADD)
        terrain_background = pygame.transform.smoothscale(terrain_background, target.get_size())
        target.blit(terrain_background, (0, 0))

    # def draw_soft_circle(self, bg: pygame.Surface, pos: Vec, rad: int, color: tuple[int, int, int]) -> Optional[pygame.Surface]:
    #     if self.pos.distance_to(pos) > self.BLEND_DISTANCE + rad + 1000: return None
    #     BLEND_NUM = 64
    #     for r in range(self.BLEND_DISTANCE + rad, rad, -int(self.BLEND_DISTANCE / BLEND_NUM)):
    #         alpha = int(255 * ( 1 - ((r - rad) / self.BLEND_DISTANCE)))
    #         pygame.draw.circle(bg, (*color, alpha), pos - self.pos, r)

    def draw_mixed_background(self, target: pygame.Surface):
        # Behold, me trying to understand numpy (hence the extra comments)
        wid, hei = target.get_size()

        # coordinate grids (These seem to be arrays..?)
        y_ind, x_ind = np.indices((hei, wid))

        # color and weight buffers (makes empty arrays I think...)
        color_buffer =  np.zeros((hei, wid, 3), dtype=np.float32)
        weight_buffer = np.zeros((hei, wid), dtype=np.float32)

        # it seems this loop is working on whole grids at once?
        for (cx, cy), rad, color in self.color_circles:
            # find distance to center of circle
            dx = x_ind + (self.pos.x - cx) / self.SCALE_FACTOR
            dy = y_ind + (self.pos.y - cy) / self.SCALE_FACTOR
            dist = np.sqrt(dx**2 + dy**2)

            # Weights of colors
            weight = np.clip(1 - ((dist - rad / self.SCALE_FACTOR) / self.BLEND_DISTANCE), 0, 1)
            weight_sq = weight**2 # smoother fade

            # Apply color
            for i in range(3): # This should be RGB range
                color_buffer[..., i] += color[i] * weight_sq

            weight_buffer += weight_sq

        # add the background green when there is not enough weight
        remaining_weight = np.clip(1 - weight_buffer, 0, 1)
        for i in range(3):
            color_buffer[..., i] += self.background[i] * remaining_weight

        # normalize final color
        total_weight = weight_buffer + remaining_weight
        final_rgb = (color_buffer / total_weight[..., None]).astype(np.uint8) # no idea how this line works
        final_rgb = final_rgb.swapaxes(0, 1)

        pygame.surfarray.blit_array(target, final_rgb)
