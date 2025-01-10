from datetime import datetime
from .debugger import Debug

class Log:
    """A simple logging class that can be used to log messages to the console.

    The class has four logging methods: `debug`, `info`, `warn`, and `error`.
    Each method takes a single argument, the message to log. The message will
    be prefixed with the type of message and the current time.

    Each method will only log if the corresponding debug type is enabled in the
    `debug.toml` file. If the file does not exist, the methods will not run.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    @Debug.requires_debug("debug")
    def debug(message: str) -> None:
        print(f"[{Log.OKBLUE}DEBUG{Log.ENDC} {Log.UNDERLINE}{Log.datetime()}{Log.ENDC}] {message}")

    @staticmethod
    @Debug.requires_debug("info")
    def info(message: str) -> None:
        print(f"[{Log.OKGREEN}INFO{Log.ENDC} {Log.UNDERLINE}{Log.datetime()}{Log.ENDC}] {message}")

    @staticmethod
    @Debug.requires_debug("warn")
    def warn(message: str) -> None:
        print(f"[{Log.WARNING}WARNING{Log.ENDC} {Log.UNDERLINE}{Log.datetime()}{Log.ENDC}] {message}")

    @staticmethod
    @Debug.requires_debug("error")
    def error(message: str) -> None:
        print(f"[{Log.BOLD}{Log.FAIL}CRITICAL{Log.ENDC} {Log.UNDERLINE}{Log.datetime()}{Log.ENDC}] {message}")

    @staticmethod
    def datetime() -> str:
        return datetime.now().strftime("%H:%M:%S.%f")

__all__ = ["Log"]
