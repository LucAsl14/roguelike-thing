from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .replayer import Replayer

from src.core.util.debug.debugger import Debug
from src.core.util.debug.logger import Log
from uuid import UUID, uuid4
from typing import Callable
import copyreg
import pickle
import pygame

class Snapshot:
    surfaces: dict[UUID, pygame.Surface] = {}

    def __init__(self, replayer: Replayer, timestamp: int) -> None:
        self.replayer = replayer
        self.timestamp = timestamp

        copyreg.pickle(pygame.Surface, self.pickle_surface)

        self.gamestate = pickle.dumps(replayer.game.scene)

        if Debug.is_debug("snapshot-info"):
            Log.info(f"Snapshot taken at timestamp {timestamp}.")

    def pickle_surface(self, surface: pygame.Surface) -> tuple[Callable, tuple]:
        uuid = uuid4()
        self.surfaces[uuid] = surface
        return self.unpickle_surface, (uuid,)

    def unpickle_surface(self, uuid: UUID) -> pygame.Surface:
        return self.surfaces[uuid]
