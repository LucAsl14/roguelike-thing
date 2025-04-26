from .player import Player

from shared.shared import SharedTemplate
sprite_classes: dict[str, type[SharedTemplate]] = {
    "Player": Player,
}
