# /// script
# dependencies = [
#   "pygame-ce",
#   "zengl",
# ]
# ///

from src.core.game import Game
import asyncio
import pygame

if __name__ == "__main__":
    pygame.init()
    asyncio.run(Game().run())
