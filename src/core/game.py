from pygame.locals import SCALED, FULLSCREEN, KEYDOWN, KEYUP, QUIT
from src.core.util.timer import Time
from src.core.scene import Scene
import src.game.scenes as scenes
from src.game.settings import *
from typing import cast, Never
from src.core.util import *
import pygame

class AbortScene(Exception):
    def __str__(self):
        return "Scene aborted but not caught with a try/except block."

class AbortGame(Exception):
    def __str__(self):
        return "Game aborted but not caught with a try/except block."

class Game(metaclass=Singleton):
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.size = self.width, self.height = self.w, self.h = WIDTH, HEIGHT
        self.screen = pygame.display.set_mode(self.size, SCALED | FULLSCREEN * (not Debug.on()))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.time = pygame.time.get_ticks() / 1000
        self.dt = self.clock.tick(0) / 1000
        self.fps = 0
        self.timestamp = 0

    def run(self) -> None:
        self.replayer = Replayer(self)
        self.scene = scenes.MainScene(self)

        while True:
            self.time = pygame.time.get_ticks() / 1000 - Debug._pause_time - self.replayer.time
            Time.begin_frame(self)
            self.seed = time()
            seed(self.seed)

            try:
                self.update()
                if not Debug.paused():
                    self.scene.update(self.dt)
            except AbortScene:
                continue
            except AbortGame:
                break

            if not Debug.paused():
                self.scene.draw(self.screen)
                Debug.draw(self)
            pygame.display.flip()

            if not self.replayer.running and not Debug.paused():
                self.replayer.record()
            self.dt = self.clock.tick(0) / 1000
            self.fps = self.clock.get_fps()
            if not self.replayer.running and not Debug.paused():
                self.timestamp += 1

        pygame.quit()

    def update(self) -> None:
        self.events = {event.type: event for event in pygame.event.get()}
        self.key_down = -1
        if KEYDOWN in self.events:
            self.key_down = cast(pygame.event.Event, self.events[KEYDOWN]).key
        self.key_up = -1
        if KEYUP in self.events:
            self.key_up = cast(pygame.event.Event, self.events[KEYUP]).key

        self.keys = pygame.key.get_pressed()
        self.mouse_pos = Vec(pygame.mouse.get_pos())
        self.mouse_pressed = pygame.mouse.get_pressed()

        if QUIT in self.events:
            raise AbortGame

        if KEYDOWN in self.events and Debug.on():
            match self.events[KEYDOWN].key:
                case pygame.K_F1:
                    if not self.replayer.running:
                        Debug.toggle_paused(self)
                case pygame.K_F2:
                    if not self.replayer.running:
                        self.replayer.replay()
                case pygame.K_F3:
                    Debug.toggle_visibility()

        Profile.update(self.key_down)

    def new_scene(self, scene: str, *args: Any, **kwargs: Any) -> Never:
        cls: Type[Scene] = getattr(scenes, scene)
        self.scene = cls(self, *args, **kwargs)
        raise AbortScene

    def set_scene(self, scene: Scene) -> Never:
        self.scene = scene
        raise AbortScene

    def __getstate__(self) -> dict:
        return {}

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(Game().__dict__)
