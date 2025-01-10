from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.game import Game

from typing import Any, Callable, Optional
from src.core.util.timer import Time
from itertools import chain
from functools import wraps
import tomllib
import pygame
import os

class Debug:
    """A simple debugging class that can be used to enable or disable debug
    output in the game.

    This class will dynamically read the `debug.toml` file and check if the
    given debug type is enabled. If the file does not exist, the debug type
    will be disabled. If a list of entries is provided in the file, the class
    will evaluate them and display the results on the screen.

    Initial formatting of the `debug.toml` file should look like this:
    ```toml
    debug = true
    info = true
    warn = true
    error = true

    [entries]
    # Name = "source"
    """

    @staticmethod
    def on() -> bool:
        return Debug.get_visibility("debug")

    @staticmethod
    def requires_debug(*types: str) -> Callable[..., Any]:
        """Any function decorated with this will only run if the given debug
        type is enabled in the debug.toml file.

        Args:
            type: The type of debug to check for. Defaults to "debug".

        Returns:
            The decorated function.

        Example:
            ```python
            @Debug.requires_debug()
            def my_function():
                print("This will only run if the 'debug' type is enabled.")

            @Debug.requires_debug("warn")
            def my_function():
                print("This will only run if the 'warn' type is enabled.")

            @Debug.requires_debug("info", "custom_type")
            def my_function():
                print("This will only run if the 'info' and 'custom_type' types are both enabled.")
            ```
        """
        types = types or ("debug",)
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                if Debug.get_visibility(*types):
                    return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def is_debug(*types: str) -> bool:
        return Debug.get_visibility(*types)

    _conf_cache = None
    _conf_last_modified = None

    @staticmethod
    def get_config_option(name: str) -> Optional[Any]:
        try:
            last_modified = os.path.getmtime("debug.toml")
            # Only read the file if it has been modified since the last read
            if Debug._conf_cache is None or Debug._conf_last_modified != last_modified:
                with open("debug.toml", "rb") as file:
                    Debug._conf_cache = tomllib.load(file)
                    Debug._conf_last_modified = last_modified
            return Debug._conf_cache.get(name)
        except FileNotFoundError:
            return None

    @staticmethod
    def get_visibility(*types: str) -> bool:
        try:
            return all(Debug.get_config_option(type) for type in types)
        except KeyError:
            return False

    _debug_entries: Optional[dict[str, str]] = {}
    _debug_font = None
    _visible = True
    _paused = False
    _pause_start = 0
    _pause_time = 0

    @staticmethod
    def toggle_visibility() -> None:
        Debug._visible = not Debug._visible

    @staticmethod
    def toggle_paused(game: Game) -> None:
        Debug._paused = not Debug._paused
        if Debug._paused:
            Debug._pause_start = pygame.time.get_ticks() / 1000
        else:
            Debug._pause_time += pygame.time.get_ticks() / 1000 - Debug._pause_start
            # Unfortunately we need to update this here as well or else for one
            # frame the time will be off, causing issues with timers and such
            game.time = pygame.time.get_ticks() / 1000 - Debug._pause_time
            Time.begin_frame(game)

    @staticmethod
    def paused() -> bool:
        return Debug._paused

    @staticmethod
    @requires_debug()
    def draw(game: Game) -> None:
        if not Debug._visible: return

        Debug._debug_entries = Debug.get_config_option("entries")
        if Debug._debug_entries is None: return

        # Define locals
        if game.replayer.running:
            scene = game.replayer.scene
        else:
            scene = game.scene

        if Debug._debug_font is None:
            Debug._debug_font = pygame.font.SysFont("monospace", 16)

        lines = chain([("fps", f"{game.fps:.1f}"),
                       ("timestamp", f"{game.timestamp}")],
                       Debug._debug_entries.items())
        for i, (name, source) in enumerate(lines):
            try:
                value = eval(source)
            except Exception as e:
                value = f"ERROR: {e}"
            text = Debug._debug_font.render(f"{name}: {value}", True, (255, 255, 255), (0, 0, 0))
            text.set_alpha(150)
            game.screen.blit(text, (0, i * 19))

__all__ = ["Debug"]
