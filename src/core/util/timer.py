from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core import Game

from typing import Optional

class Time:
    _time = 0

    @staticmethod
    def begin_frame(game: Game) -> None:
        Time._time = game.time

    @staticmethod
    def time() -> float:
        return Time._time

time = Time.time # Alias for convenience

class Timer():
    """A timer class that lasts for a certain duration.

    Args:
        duration: The duration of the timer in seconds.
    """

    def __init__(self, duration: float) -> None:
        self.duration = duration
        self.time = time()
        self.paused = False

    @property
    def elapsed(self) -> float:
        """The time elapsed since the timer started."""
        return time() - self.time

    @property
    def remaining(self) -> float:
        """The time remaining until the timer is done."""
        return self.duration - self.elapsed

    @property
    def progress(self) -> float:
        """The progress of the timer as a value between 0 and 1."""
        return self.elapsed / self.duration

    @property
    def progress_remaining(self) -> float:
        """The progress remaining until the timer is done as a value between 0
        and 1.
        """
        return self.remaining / self.duration

    @property
    def done(self) -> bool:
        """Whether the timer is done."""
        return self.elapsed >= self.duration and not self.paused

    def reset(self, duration: Optional[float] = None) -> None:
        """Reset the timer to a new duration. If no duration is provided, the
        timer is reset to the original duration.

        Args:
            duration: The new duration of the timer in seconds.
        """
        if duration is not None:
            self.duration = duration
        self.time = time()

    def pause(self) -> None:
        """Pause the timer."""
        self.duration -= self.elapsed
        self.paused = True

    def resume(self) -> None:
        """Resume the timer."""
        self.time = time()
        self.paused = False

    def toggle(self) -> None:
        """Toggle the timer between paused and resumed."""
        if self.paused:
            self.resume()
        else:
            self.pause()

    def force_end(self) -> None:
        """Force the timer to end."""
        self.time = time() - self.duration

    def __repr__(self) -> str:
        return f"Timer({self.duration})"

    def __str__(self) -> str:
        return f"Timer({self.duration})"

    def __bool__(self) -> bool:
        """Whether the timer is running."""
        return not self.done

class LoopTimer(Timer):
    """A timer class that lasts for a certain duration and loops a certain
    number of times.

    Args:
        duration: The duration of the timer in seconds.
        max_loops: The maximum number of loops the timer can do. If this is -1,
            the timer will loop infinitely.
    """

    def __init__(self, duration: float, max_loops: int = -1) -> None:
        super().__init__(duration)
        self.max_loops = max_loops
        self.loops = 0

    @property
    def done(self) -> bool:
        """Whether the timer is done. If the timer is done, it will be reset if
        it hasn't reached the max number of loops yet.
        """
        if self.paused: return False
        if not super().done: return False

        self.loops += 1
        # If the timer is done, reset it only if it hasn't reached the max
        # number of loops yet.
        if self.max_loops == -1 or self.loops < self.max_loops:
            self.reset()

        # For one frame, the timer is done, but it will be reset in the next
        # frame if it hasn't reached the max number of loops yet.
        return True

    def reset(self, duration: Optional[float] = None) -> None:
        """Reset the timer to a new duration and reset the number of loops. If
        no duration is provided, the timer is reset to the original duration.

        Args:
            duration: The new duration of the timer in seconds.
        """
        super().reset(duration)
        self.loops = 0

    def __repr__(self) -> str:
        return f"LoopTimer({self.duration}, {self.max_loops})"

    def __str__(self) -> str:
        return f"LoopTimer({self.duration}, {self.max_loops})"

class PreciseLoopTimer(LoopTimer):
    """A more precise version of the loop timer that accounts for the time
    elapsed between frames, and corrects the timer to start from the correct
    time in the next frame. In the case of timer durations shorter than the
    frame time, this timer will loop the correct number of times, while the
    regular loop timer will not.

    The number of loops that have elapsed since the last frame is stored in the
    `subframe_loops` attribute, which may be accessed after the timer is done
    to get the number of loops that have elapsed since the last frame. This
    attribute may be used to perform the action multiple times in case the
    timer finished more than once in a single frame.

    Args:
        duration: The duration of the timer in seconds.
        max_loops: The maximum number of loops the timer can do. If this is -1,
            the timer will loop infinitely.
    """

    def __init__(self, duration: float, max_loops: int = -1) -> None:
        super().__init__(duration, max_loops)
        self.subframe_loops = 0

    @property
    def done(self) -> bool:
        """Whether the timer is done. If the timer is done, it will be reset if
        it hasn't reached the max number of loops yet. The number of loops that
        have elapsed since the last frame is stored in the `subframe_loops`
        attribute.
        """
        if self.paused: return False

        # The number of loops that have elapsed since the last frame.
        self.subframe_loops = int(self.elapsed // self.duration)
        # If the timer is infinite, the number of loops is the number of loops
        # that have elapsed since the last frame, nothing needs to be done.
        if self.max_loops != -1:
            # If the timer is finite, the number of loops may cause the total
            # number of loops to exceed the maximum number of loops allowed,
            # so the number of loops is clamped to the maximum number of loops
            # allowed.
            self.subframe_loops = min(
                self.subframe_loops,
                self.max_loops - self.loops
            )

        self.loops += self.subframe_loops
        # Advance the start time by the number of loops that have elapsed since
        # the last frame times the duration of the timer, so that the timer
        # starts from the correct time in the next frame. This needs to be done
        # instead of just resetting the timer, because the last loop of the
        # timer within the frame may not have finished yet.
        self.time += self.subframe_loops * self.duration

        return self.subframe_loops > 0

    def __repr__(self) -> str:
        return f"PreciseLoopTimer({self.duration})"

    def __str__(self) -> str:
        return f"PreciseLoopTimer({self.duration})"

__all__ = [
    "Time",
    "time",
    "Timer",
    "LoopTimer",
    "PreciseLoopTimer"
]
