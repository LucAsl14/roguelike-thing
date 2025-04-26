from .player import Player

from shared.shared import SharedTemplate
# This is basically a mapping from the string type that the client receive from
# the server TO the class of the sprite the client should use to represent it.
sprite_classes: dict[str, type[SharedTemplate]] = {
    "Player": Player,
}
