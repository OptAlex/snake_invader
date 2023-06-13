from help_functions.const import BULLET_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT, SEGMENT_SIZE
import pyglet
from pyglet.sprite import Sprite
import random

class FallingObject:
    def __init__(self, image_path):
        self.image = pyglet.image.load(image_path)
        self.sprite = pyglet.sprite.Sprite(
            self.image,
            x=random.randint(0, WINDOW_WIDTH // SEGMENT_SIZE - 1) * SEGMENT_SIZE + SEGMENT_SIZE // 2,
            y=WINDOW_HEIGHT - BULLET_SPEED + SEGMENT_SIZE // 2
        )

    def move(self):
        self.sprite.y -= SEGMENT_SIZE

    def draw(self):
        """Draws the object on the screen."""
        self.sprite.draw()

    def is_off_screen(self):
        """Checks if the object is off the screen."""
        return self.sprite.y < 0


class Bullet(FallingObject):
    def __init__(self):
        super().__init__('pictures/bullet.png')


class Heart(FallingObject):
    def __init__(self):
        super().__init__('pictures/heart.png')
