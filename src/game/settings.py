from enum import Enum, auto
from src.core.util.general import pathof
import pygame


class Layer(Enum):
    BACKGROUND = auto()
    GROUND = auto()
    DEFAULT = auto()
    SKY = auto()
    HUD = auto()

TITLE = "Game"
WIDTH = 960
HEIGHT = 540
SIZE = WIDTH, HEIGHT
