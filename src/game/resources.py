from src.core.util import Resource, Image, Sound, Font, VertShader, FragShader

def init_resources() -> None:
    Image("test", "test.png", scale=1)
    Image("player", "player.png", scale=1)
    Image("spawnpoint", "spawnpoint.png", scale=1)
    Image("death_screen", "death_screen.png", scale=1)
    Image("city", "city.png", scale=1)

    VertShader("default", "default.vert")
    FragShader("default", "default.frag")

    for i in range(1, 129):
        Font(f"font{i}", "PixelTandysoft-0rJG.ttf", i)
