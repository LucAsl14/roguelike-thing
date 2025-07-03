from __future__ import annotations
from src.core import *

class DeathScreen(Sprite): # this should REALLY be a scene, but for now it's a sprite because goddamnit I can't get it to work otherwise
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, "HUD")
        # for some reason pausing is also broken, so I have to put a frame counter here
        # ALSO, extra jank because of this being a sprite, you can only get out of "dead mode" by pressing F1 in debug mode lmao
        self.frame_count = 0

    def update(self, dt: float) -> None:
            if self.frame_count == 2:
                Log.debug("success")
                Debug.unpause(self.game)
                self.frame_count = -9999
                self.kill()

    def draw(self, target: pygame.Surface) -> None:
        target.blit(Image.get("death_screen"))
        self.frame_count += 1
        if self.frame_count == 2:
            Debug.pause(self.game)
            Log.debug("paused")
