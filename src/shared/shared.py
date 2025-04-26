from typing import Any, Generator, TypedDict
from functools import cached_property
from util.vector import Vec
from abc import ABCMeta
import json

class Message(TypedDict):
    uuid: str
    type: str
    recipient: str
    content: Any

def backup_encoder(obj: Any) -> dict:
    if hasattr(obj, "serialize"):
        return obj.serialize()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable.")

def backup_decoder(obj: dict) -> Any:
    if obj.get("_type", None) == "Vec":
        return Vec(obj["x"], obj["y"])
    return obj

def serialize(message: Message) -> str:
    return json.dumps(
        message,
        separators=(",", ":"),
        default=backup_encoder
    )

class SharedTemplateMeta(ABCMeta):
    _sync_fields: list[str] = []

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        annotations = {}
        for base in reversed(cls.__mro__):
            annotations.update(getattr(base, "__annotations__", {}))
        cls._sync_fields = list(annotations.keys())
        return cls

class SharedTemplate(metaclass=SharedTemplateMeta):
    uuid: str = ""

    @cached_property
    def _type(self) -> str:
        for base in reversed(self.__class__.__mro__):
            if base.__name__.startswith("T_"):
                return base.__name__.lstrip("T_")
        return "UNKNOWN"

    def get_attributes(self) -> Generator[tuple[str, Any], None, None]:
        yield "_type", self._type
        for field in self._sync_fields:
            if not field.startswith("_"):
                yield field, getattr(self, field)

    def apply(self, json_data: dict[str, Any]) -> None:
        for key, value in json_data.items():
            if not key.startswith("_"):
                setattr(self, key, value)

class Outgoing(SharedTemplate):
    """Sprites can be marked as outgoing. This means that any changes to their
    relevant attributes will be sent to the server. This is primarily used for
    player input, but can be used for other things as well."""
    pass
