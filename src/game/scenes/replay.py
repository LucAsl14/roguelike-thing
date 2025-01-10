from __future__ import annotations
from src.core import *
from src.game.sprites import *

class Replay(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.previous_scene = game.scene
        self.replayer = game.replayer

        self.previous_caption = pygame.display.get_caption()
        pygame.display.set_caption(f"{self.previous_caption[0]} - REPLAY")

        Log.info(f"Replay started at timestamp {self.replayer.timestamp}.")

    def update(self, dt: float) -> None:
        if pygame.KEYDOWN in self.game.events:
            match self.game.events[pygame.KEYDOWN].key:
                case pygame.K_ESCAPE:
                    self.quit()
                case pygame.K_F1 | pygame.K_SPACE:
                    self.replayer.pause()
                case pygame.K_LEFT:
                    self.replayer.seek_previous_snapshot()
                case pygame.K_RIGHT:
                    self.replayer.seek_next_snapshot()
                case pygame.K_PERIOD:
                    self.replayer.step_forward()

        self.replayer.update_replay()
        if not self.replayer.paused:
            self.replayer.next_timestamp()

        self.sprite_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.replayer.view, (0, 0))

        self.sprite_manager.draw(screen)

    def quit(self) -> Never:
        self.replayer.quit()
        pygame.display.set_caption(*self.previous_caption)
        self.game.set_scene(self.previous_scene)
