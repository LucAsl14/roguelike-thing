from .render_layer import LayerGroup, Layer
from client.settings import *
from .network import Network
from .sprite import Sprite
from .scene import Scene
from .resource import *
from .debug import *
from util import *
import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game import Game
    from scenes import *
