from client.core import *

class Camera(Sprite):
    def __init__(self, scene: Scene, target: Sprite) -> None:
        super().__init__(scene, "DEFAULT")
        self.target = target
        self.pos = self.target.pos - self.game.size / 2 + self.target.size / 2

    def update(self, dt: float) -> None:
        offset = self.target.pos - self.game.size / 2 - self.pos + self.target.size / 2
        self.pos += offset * 6 * dt

    def draw(self, target: pygame.Surface) -> None:
        pass
