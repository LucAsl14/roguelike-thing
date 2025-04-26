from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from client.core.scene import Scene

from client.core.resource import VertShader, FragShader
from client.core.sprite import Sprite
from typing import Any, Type
import pygame
import zengl

class LayerGroupRecord:
    def __init__(self, type: Type[LayerGroup], vert: str, frag: str) -> None:
        self.type = type
        self.vert = vert
        self.frag = frag
        self.layers: list[LayerRecord] = []

    def add(self, *layers: LayerRecord) -> LayerGroupRecord:
        self.layers.extend(layers)
        return self

    def construct(self, scene: Scene) -> LayerGroup:
        group = self.type(scene, vert=self.vert, frag=self.frag)
        group.layers = [layer.construct(scene) for layer in self.layers]
        return group

class LayerGroup:
    @classmethod
    def record(cls, vert: str = "default", frag: str = "default") -> LayerGroupRecord:
        return LayerGroupRecord(cls, vert, frag)

    def __init__(self, scene: Scene, vert: str = "default", frag: str = "default") -> None:
        self.game = scene.game
        self.vert = vert
        self.frag = frag
        self.layers: list[Layer] = []

        self.image = self.game.ctx.image(self.game.size.itup, "rgba8unorm")
        self.pipeline = self._create_pipeline()
        self.surface = pygame.Surface(self.game.size, pygame.SRCALPHA)

    def _create_pipeline(self) -> zengl.Pipeline:
        return self.game.ctx.pipeline(
            vertex_shader=VertShader.get(self.vert),
            fragment_shader=FragShader.get(self.frag),
            framebuffer=None,
            viewport=(0, 0, *self.game.size.itup),
            topology="triangle_strip",
            vertex_count=4,
            blend={
                "enable": True,
                "src_color": "src_alpha",
                "dst_color": "one_minus_src_alpha",
                "src_alpha": "one",
                "dst_alpha": "one_minus_src_alpha",
            },
            resources=[
                {
                    "type": "sampler",
                    "binding": 0,
                    "image": self.image,
                    "min_filter": "nearest",
                    "mag_filter": "nearest",
                    "wrap_x": "clamp_to_edge",
                    "wrap_y": "clamp_to_edge",
                },
            ],
            layout=[
                {
                    "name": "u_texture",
                    "binding": 0,
                },
            ]
        )

    def update(self, dt: float) -> None:
        for layer in self.layers:
            layer.update(dt)

    def draw(self) -> None:
        for layer in self.layers:
            layer.draw(self.surface)

        self.image.write(pygame.image.tobytes(self.surface, "RGBA", True))
        self.pipeline.render()

class LayerRecord:
    def __init__(self, type: Type[Layer], *args: Any, **kwargs: dict[str, Any]) -> None:
        self.type = type
        self.args = args
        self.kwargs = kwargs

    def construct(self, scene: Scene) -> Layer:
        return self.type(scene, *self.args, **self.kwargs)

class Layer:
    @classmethod
    def record(cls, name: str, pixel_scale: int = 1) -> LayerRecord:
        return LayerRecord(cls, name, pixel_scale)

    def __init__(self, scene: Scene, name: str, pixel_scale: int = 1) -> None:
        self.game = scene.game
        self.name = name
        self.pixel_scale = pixel_scale
        self.updating: list[Sprite] = []
        self.drawing: list[Sprite] = []

    def update(self, dt: float) -> None:
        for sprite in self.updating:
            sprite.update(dt)

    def draw(self, target: pygame.Surface) -> None:
        for sprite in self.drawing:
            sprite.draw(target)

    def add(self, sprite: Sprite) -> None:
        self.updating.append(sprite)
        self.drawing.append(sprite)

    def remove(self, sprite: Sprite) -> None:
        self.updating.remove(sprite)
        self.drawing.remove(sprite)
