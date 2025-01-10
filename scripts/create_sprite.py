import os
import re

LOCAL_PATH = os.path.dirname(__file__)
SPRITES_PATH = os.path.join(LOCAL_PATH, "..", "src", "game", "sprites")
INIT_PATH = os.path.join(SPRITES_PATH, "__init__.py")
TEMPLATE_PATH = os.path.join(LOCAL_PATH, "sprite_template.txt")

PASCAL_REGEX = r"^[A-Z][a-zA-Z0-9]*$"
SCREAMING_SNAKE_REGEX = r"^[A-Z0-9]+(?:_[A-Z0-9]+)*$"
SNAKE_REGEX_SUB = r"([a-z0-9])([A-Z])", r"\1_\2"

def get_name() -> str:
    while True:
        name = input("Enter the name of the sprite: ").strip()
        if re.match(PASCAL_REGEX, name):
            break
        print("Invalid name. Must be in PascalCase and follow Python's naming conventions.")
    return name

def get_super() -> str:
    while True:
        superclass = input("Enter the name of the superclass (default: Sprite): ").strip()
        superclass = superclass or "Sprite"
        if re.match(PASCAL_REGEX, superclass):
            break
        print("Invalid name. Must be in PascalCase and follow Python's naming conventions.")
    return superclass

def get_scene() -> str:
    while True:
        scene = input("Enter the name of the scene (default: MainScene): ").strip()
        scene = scene or "MainScene"
        if re.match(PASCAL_REGEX, scene):
            break
        print("Invalid name. Must be in PascalCase and follow Python's naming conventions.")
    return scene

def get_layer() -> str:
    while True:
        layer = input("Enter the layer of the sprite: ").strip()
        if re.match(SCREAMING_SNAKE_REGEX, layer):
            break
        print("Invalid name. Must be in SCREAMING_SNAKE_CASE and follow Python's naming conventions.")
    return layer

def create_sprite(name: str, superclass: str, scene: str, layer: str) -> str:
    snake_name = re.sub(*SNAKE_REGEX_SUB, name).lower()

    sprite_path = os.path.join(SPRITES_PATH, f"{snake_name}.py")

    with open(TEMPLATE_PATH, "r") as template, open(sprite_path, "w") as sprite:
        content = template.read() % {
            "name": name,
            "super": superclass,
            "scene": scene,
            "layer": layer,
        }
        sprite.write(content)

    with open(INIT_PATH, "a") as init:
        init.write(f"from .{snake_name} import {name}\n")

    return sprite_path

def main() -> None:
    path = create_sprite(get_name(), get_super(), get_scene(), get_layer())
    print(f"Sprite created at {path}.")

if __name__ == "__main__":
    main()
