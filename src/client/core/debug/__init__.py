from typing import Callable, Any
import sys
import os

if sys.platform.startswith("emscripten"):
    class DummyProfile:
        """Dummy profiler class for platforms that don't support profiling."""
        @classmethod
        def update(cls, key: int) -> None:
            pass

        @classmethod
        def toggle(cls) -> None:
            pass

        @classmethod
        def select(cls, index: int) -> None:
            pass

        @classmethod
        def clear(cls) -> None:
            pass

        def __init__(self, func: Callable, _save: bool = True, _print: bool = False) -> None:
            self.func = func

        def __call__(self, *args, **kwargs) -> None:
            self.func(*args, **kwargs)

    Profile = DummyProfile

    class DummyDebug:
        """Dummy debugger class for platforms that don't support debugging."""
        @classmethod
        def on(cls) -> bool:
            return False

        @classmethod
        def paused(cls) -> bool:
            return False

        @classmethod
        def toggle_paused(cls, game: object) -> None:
            pass

        @classmethod
        def launch_tkinter_tree(cls, game: object) -> None:
            pass

        _pause_time = 0

    Debug = DummyDebug

    class DummyLog:
        """Dummy logger class for platforms that don't support logging."""
        LOG_FILE = "debug.log"

        @classmethod
        def info(cls, message: str) -> None:
            pass

        @classmethod
        def error(cls, message: str) -> None:
            pass

        @classmethod
        def debug(cls, message: str) -> None:
            pass

        @classmethod
        def warning(cls, message: str) -> None:
            pass

        @classmethod
        def watch(cls, value: Any) -> None:
            pass

    Log = DummyLog
else:
    from .profiler import Profile
    from .debugger import Debug
    from .logger import Log

if not os.path.exists("debug"):
    os.makedirs("debug")
if not os.path.exists("debug/profiles"):
    os.makedirs("debug/profiles")

with open(Log.LOG_FILE, "w") as log_file:
    log_file.write("")
