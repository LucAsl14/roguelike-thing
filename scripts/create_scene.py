import os
import re

LOCAL_PATH = os.path.dirname(__file__)
SCENES_PATH = os.path.join(LOCAL_PATH, "..", "src", "game", "scenes")
INIT_PATH = os.path.join(SCENES_PATH, "__init__.py")
TEMPLATE_PATH = os.path.join(LOCAL_PATH, "scene_template.txt")

PASCAL_REGEX = r"^[A-Z][a-zA-Z0-9]*$"
SNAKE_REGEX_SUB = r"([a-z0-9])([A-Z])", r"\1_\2"

def get_name() -> str:
    while True:
        name = input("Enter the name of the scene: ").strip()
        if re.match(PASCAL_REGEX, name):
            break
        print("Invalid name. Must be in PascalCase and follow Python's naming conventions.")
    return name

def create_sprite(name: str) -> str:
    snake_name = re.sub(*SNAKE_REGEX_SUB, name).lower()

    scene_path = os.path.join(SCENES_PATH, f"{snake_name}.py")

    with open(TEMPLATE_PATH, "r") as template, open(scene_path, "w") as scene:
        content = template.read() % {
            "name": name,
        }
        scene.write(content)

    with open(INIT_PATH, "a") as init:
        init.write(f"from .{snake_name} import {name}\n")

    return scene_path

def main() -> None:
    path = create_sprite(get_name())
    print(f"Scene created at {path}.")

if __name__ == "__main__":
    main()
