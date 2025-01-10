from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.scene import Scene
    from .replayer import Replayer
    from .snapshot import Snapshot

from pygame.constants import KEYDOWN, KEYUP
from src.core.util.timer import Time
from typing import Optional, cast
import pickle
import pygame

class Frame:
    def __init__(self, replayer: Replayer, snapshot: Optional[Snapshot], timestamp: int) -> None:
        self.replayer = replayer
        self.snapshot = snapshot
        self.timestamp = timestamp

        self.game = replayer.game
        self.dt = self.game.dt
        self.time = self.game.time
        self.timestamp = self.game.timestamp
        self.fps = self.game.fps
        self.events = self.game.events.copy()
        self.keys = self.game.keys
        self.mouse_pos = self.game.mouse_pos
        self.mouse_pressed = self.game.mouse_pressed
        self.seed = self.game.seed

    def apply(self) -> Optional[Scene]:
        self.game.dt = self.dt
        self.game.time = self.time
        self.game.timestamp = self.timestamp
        Time.begin_frame(self.game)
        self.game.fps = self.fps
        self.game.events = self.events
        self.game.key_down = -1
        if KEYDOWN in self.events:
            self.key_down = cast(pygame.event.Event, self.game.events[KEYDOWN]).key
        self.key_up = -1
        if KEYUP in self.events:
            self.key_up = cast(pygame.event.Event, self.game.events[KEYUP]).key
        self.game.keys = self.keys
        self.game.mouse_pos = self.mouse_pos
        self.game.mouse_pressed = self.mouse_pressed
        self.game.seed = self.seed

        if self.snapshot:
            return pickle.loads(self.snapshot.gamestate)
        return None
