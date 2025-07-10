from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from src.core.util.timer import Time
from typing import Any, Callable
from functools import wraps
from tkinter import ttk
from .logger import Log
import tkinter as tk
import tomllib
import weakref
import pygame
import types

class ToolTip:
    def __init__(self, widget: tk.Widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None

    def showtip(self, text: str, x: int, y: int) -> None:
        """Display text in tooltip window with wrapping."""
        self.hidetip()
        self.tipwindow = tk.Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(True)
        self.tipwindow.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tipwindow, text=text, justify=tk.LEFT,
            background="#ffffe0", relief=tk.SOLID, borderwidth=1,
            font="tahoma 8 normal",
            wraplength=600
        )
        label.pack(ipadx=1)

    def hidetip(self) -> None:
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None

class Debug:
    _categories: dict[str, bool] = {}

    try:
        with open("debug.toml", "rb") as file:
            data = tomllib.load(file)
            _categories.update(data)
    except FileNotFoundError:
        pass # Debug is off

    @staticmethod
    def requires_debug(*categories: str) -> Callable[..., Any]:
        """Any function decorated with this will only run if the given debug
        category is enabled.

        Args:
            category: The category of debug to check for. Defaults to "debug".

        Returns:
            The decorated function.

        Example:
            ```python
            @Debug.requires_debug()
            def my_function():
                print("This will only run if the 'debug' category is enabled.")

            @Debug.requires_debug("hitbox")
            def my_function():
                print("This will only run if the 'hitbox' category is enabled.")

            @Debug.requires_debug("info", "custom")
            def my_function():
                print("This will only run if the 'info' and 'custom' categories are both enabled.")
            ```
        """
        categories += ("debug",)
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                if Debug.get_category(*categories):
                    return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    @requires_debug()
    def toggle_category(category: str) -> None:
        val = Debug._categories[category] = not Debug.get_category(category)
        Log.info(f"Toggled debug category '{category}' to {val}")

    @staticmethod
    def get_category(*categories: str) -> bool:
        return all(Debug._categories.get(category, False)
                   for category in categories)

    on = get_category # alias

    _debug_font = None
    _paused = False
    _pause_start = 0
    _pause_time = 0

    @staticmethod
    def toggle_paused(game: Game) -> None:
        """Toggles the paused state of the game. If the game is paused, it
        will be unpaused and vice versa."""
        if Debug._paused:
            Debug.unpause(game)
        else:
            Debug.pause(game)

    @staticmethod
    def pause(game: Game) -> None:
        """Pauses the game and updates the time to reflect the pause."""
        Debug._paused = True
        Debug._pause_start = pygame.time.get_ticks() / 1000

    @staticmethod
    def unpause(game: Game) -> None:
        """Unpauses the game and updates the time to reflect the unpause."""
        Debug._paused = False
        Debug._pause_time += pygame.time.get_ticks() / 1000 - Debug._pause_start
        # Unfortunately we need to update this here as well or else for one
        # frame the time will be off, causing issues with timers and such
        game.time = pygame.time.get_ticks() / 1000 - Debug._pause_time
        Time.begin_frame(game)

    @staticmethod
    def paused() -> bool:
        return Debug._paused

    @staticmethod
    def launch_tkinter_tree(game: Game) -> None:
        """Launch a tkinter interface showing a tree of attributes under the
        root scene object."""
        weak_mapping = weakref.WeakValueDictionary()
        strong_mapping = {}

        def populate_tree(tree: ttk.Treeview, parent: str, obj: Any) -> None:
            """Recursively populate the tree with attributes of the object,
            skipping only methods and weak proxy types."""
            # Handle attributes of objects
            if hasattr(obj, "__dict__"):
                for attr in dir(obj):
                    if attr.startswith("_"):
                        continue
                    value = getattr(obj, attr)
                    if isinstance(value, (types.FunctionType,
                                          types.MethodType,
                                          types.BuiltinFunctionType,
                                          weakref.ProxyType)):
                        continue

                    node = tree.insert(parent, "end", text=attr, values=(repr(value),))

                    # Store the actual object reference
                    try:
                        weak_mapping[node] = value
                    except TypeError:
                        # If object not weak-referencable, store a strong ref
                        strong_mapping[node] = value

                    # Insert dummy child to allow for expansion
                    if hasattr(value, "__dict__") or isinstance(value, (list, dict)):
                        tree.insert(node, "end")

            # Handle lists
            if isinstance(obj, list):
                for index, item in enumerate(obj):
                    node = tree.insert(parent, "end", text=f"[{index}]", values=(repr(item),))
                    # Store the actual object reference
                    try:
                        weak_mapping[node] = item
                    except TypeError:
                        strong_mapping[node] = item
                    # Insert dummy child for expandable items
                    if hasattr(item, "__dict__") or isinstance(item, (list, dict)):
                        tree.insert(node, "end")

            # Handle dictionaries
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    node = tree.insert(parent, "end", text=f"{repr(key)}", values=(repr(value),))
                    # Store the actual object reference
                    try:
                        weak_mapping[node] = value
                    except TypeError:
                        strong_mapping[node] = value
                    # Insert dummy child for expandable items
                    if hasattr(value, "__dict__") or isinstance(value, (list, dict)):
                        tree.insert(node, "end")

        def on_expand(event: Any) -> None:
            """Handle the event when a tree node is expanded."""
            item = tree.focus()
            tree.delete(*tree.get_children(item))
            # Lookup the object reference in both mappings
            obj = weak_mapping.get(item)
            if obj is None:
                obj = strong_mapping.get(item)
            if obj is not None:
                populate_tree(tree, item, obj)

        def on_motion(event: Any) -> None:
            """Update tooltip when hovering over a tree item."""
            item = tree.identify("item", event.x, event.y)
            if item:
                value = tree.item(item, "values")[0]
                tooltip.showtip(value, event.x_root + 20, event.y_root + 10)
            else:
                tooltip.hidetip()

        def on_leave(event: Any) -> None:
            """Hide tooltip when leaving the tree."""
            tooltip.hidetip()

        root = tk.Tk()
        root.geometry("500x800")
        root.title("Debug Tree Viewer")

        tree = ttk.Treeview(root, columns=("Value",), show="tree headings")
        tree.heading("#0", text="Attribute")
        tree.heading("Value", text="Value")
        tree.column("#0", width=200, stretch=False)
        tree.column("Value", stretch=True)
        populate_tree(tree, "", game)

        tooltip = ToolTip(tree)

        tree.bind("<Double-1>", on_expand)
        tree.bind("<<TreeviewOpen>>", on_expand)
        tree.bind("<Motion>", on_motion)
        tree.bind("<Leave>", on_leave)

        tree.pack(fill=tk.BOTH, expand=True)

        Debug.pause(game)
        def on_close() -> None:
            """Unpause the game when the window is closed."""
            Debug.unpause(game)
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_close)
        root.mainloop()

    _entries: dict[str, Any] = {}

    @staticmethod
    @requires_debug("info")
    def add_entry(name: str, value: Any) -> None:
        Debug._entries[name] = value

    @staticmethod
    @requires_debug("info")
    def draw(target: pygame.Surface) -> None:
        if Debug._debug_font is None:
            Debug._debug_font = pygame.font.SysFont("monospace", 16)

        for i, (name, value) in enumerate(Debug._entries.items()):
            text = Debug._debug_font.render(f"{name}: {value}", True, (255, 255, 255), (0, 0, 0))
            text.set_alpha(150)
            target.blit(text, (0, i * 19))

        Debug._entries.clear()

__all__ = ["Debug"]
