from datetime import datetime
from typing import Any

class Log:
    """A simple logging class that can be used to log messages to the console.

    The class has four logging methods: `debug`, `info`, `warn`, and `error`.
    Each method takes a single argument, the message to log. The message will
    be prefixed with the type of message and the current time.
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

    LOG_FILE = "debug/watch.txt"

    @staticmethod
    def info(*messages: str) -> None:
        level = f"{Log.OKGREEN}INFO{Log.ENDC}"
        timestamp = f"{Log.UNDERLINE}{Log.datetime()}{Log.ENDC}"
        message = " ".join(map(str, messages))
        print(f"[{level} {timestamp}] {message}")

    @staticmethod
    def warn(*messages: str) -> None:
        level = f"{Log.WARNING}WARNING{Log.ENDC}"
        timestamp = f"{Log.UNDERLINE}{Log.datetime()}{Log.ENDC}"
        message = " ".join(map(str, messages))
        print(f"[{level} {timestamp}] {message}")

    @staticmethod
    def error(*messages: str) -> None:
        level = f"{Log.FAIL}ERROR{Log.ENDC}"
        timestamp = f"{Log.UNDERLINE}{Log.datetime()}{Log.ENDC}"
        message = " ".join(map(str, messages))
        print(f"[{level} {timestamp}] {message}")

    @staticmethod
    def watch(value: Any) -> None:
        """Logs the given value to a file using the info log level."""
        timestamp = Log.datetime()
        message = f"[INFO {timestamp}] {value}"
        with open(Log.LOG_FILE, "a") as log_file:
            log_file.write(message + "\n")

    @staticmethod
    def datetime() -> str:
        return datetime.now().strftime("%H:%M:%S.%f")

__all__ = ["Log"]
