from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core import Game

from src.core.util.debug.debugger import Debug
from src.core.util.debug.logger import Log
from src.core.util.timer import LoopTimer
from src.core.util import ref_proxy
from .snapshot import Snapshot
from typing import Optional
from .frame import Frame
import pygame

class Replayer:
    def __init__(self, game: Game) -> None:
        self.game = ref_proxy(game)
        self.frames: dict[int, Frame] = {}
        self.newest_frame = 0

        # Whether the replayer is currently replaying the recorded scene
        self.running = False
        self.start_time = 0.0 # Time the current replay session was started
        self.time = 0.0 # Total time spent in all replay sessions
        # Whether the replay is paused, this acts the same as the pause in game
        # except that this will retain game-based debug information like game.time
        self.paused = False

        self.snapshot_timer = LoopTimer(5)
        self.snapshot_timer.force_end()

    @Debug.requires_debug()
    def record(self) -> None:
        """Called every frame to record the game state."""
        snapshot = None
        if self.snapshot_timer.done:
            snapshot = Snapshot(self, self.game.timestamp)
        self.frames[self.game.timestamp] = Frame(self, snapshot, self.game.timestamp)
        self.newest_frame = self.game.timestamp

    def replay(self) -> None:
        self.original_timestamp = self.game.timestamp
        self.timestamp = self.game.timestamp - 1
        while self.get_snapshot(self.timestamp) is None:
            self.timestamp -= 1
        self.view = pygame.Surface(self.game.size)
        self.running = True

        self.game.new_scene("Replay")

    def quit(self) -> None:
        self.running = False
        self.snapshot_timer.force_end()
        self.time += self.game.time - self.start_time
        self.game.timestamp = self.original_timestamp

        Log.info("Replay ended.")

    def pause(self) -> None:
        self.paused = not self.paused

    def get_frame(self, timestamp: int) -> Frame:
        return self.frames[timestamp]

    def get_snapshot(self, timestamp: int) -> Optional[Snapshot]:
        return self.frames[timestamp].snapshot

    def next_timestamp(self) -> None:
        self.timestamp += 1

    def update_replay(self) -> None:
        try:
            self.frame = self.game.replayer.get_frame(self.timestamp)
        except KeyError:
            self.paused = True

        scene = self.frame.apply()
        if scene is not None:
            self.scene = scene
        if not self.paused:
            self.scene.update(self.frame.dt)
        self.scene.draw(self.view)

    def step_forward(self) -> None:
        self.timestamp += 1
        if self.timestamp > self.game.replayer.newest_frame:
            self.timestamp = self.game.replayer.newest_frame
            return

        frame = self.game.replayer.get_frame(self.timestamp)
        if frame is None:
            self.paused = True
        else:
            self.frame = frame
        scene = self.frame.apply()
        if scene is not None:
            self.scene = scene
        self.scene.update(self.frame.dt)
        self.scene.draw(self.view)

    def seek_previous_snapshot(self) -> None:
        self.timestamp -= 1
        try:
            while self.game.replayer.get_snapshot(self.timestamp) is None:
                self.timestamp -= 1
                if self.timestamp < 0:
                    self.timestamp = 0
                    break
        except KeyError:
            self.timestamp = 0
        self.update_replay()
        self.paused = True

    def seek_next_snapshot(self) -> None:
        self.timestamp += 1
        while self.game.replayer.get_snapshot(self.timestamp) is None:
            self.timestamp += 1
            if self.timestamp > self.game.replayer.newest_frame:
                self.seek_previous_snapshot()
                return
        self.update_replay()
        self.paused = True

    def __getstate__(self) -> dict:
        # Do not include the replayer in any pickle
        return {}
