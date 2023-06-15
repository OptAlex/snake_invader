from help_functions.const import (
    FALLING_OBJ_SPEED,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    SEGMENT_SIZE,
)
import pyglet
import random


class FallingObject:
    """
    Represents an object that falls from the top of the screen.
    """

    def __init__(self, image_path):
        """
        Initializes a FallingObject instance with a given image path.

        Args:
            image_path: The path to the image file for this object.
        """
        self.image = pyglet.image.load(image_path)
        self.sprite = pyglet.sprite.Sprite(
            self.image,
            x=random.randint(0, WINDOW_WIDTH // SEGMENT_SIZE - 1) * SEGMENT_SIZE
            + SEGMENT_SIZE // 2,
            y=WINDOW_HEIGHT - FALLING_OBJ_SPEED + SEGMENT_SIZE // 2,
        )

    def move(self):
        """
        Moves the object down by the size of one segment.
        """
        self.sprite.y -= FALLING_OBJ_SPEED

    def draw(self):
        """
        Draws the object on the screen.
        """
        self.sprite.draw()

    def is_off_screen(self):
        """
        Checks if the object has fallen off the screen.

        Returns:
            A boolean indicating whether the object is off screen.
        """
        return self.sprite.y < 0


class Bullet(FallingObject):
    """
    Represents a bullet falling from the top of the screen.
    """

    def __init__(self):
        super().__init__("pictures/bullet.png")


class Heart(FallingObject):
    """
    Represents a heart falling from the top of the screen.
    """

    def __init__(self):
        super().__init__("pictures/heart.png")

    def move(self):
        """
        Moves the object down by the size of one segment.
        """
        self.sprite.y -= 0.5 * FALLING_OBJ_SPEED


class SuperBullet(FallingObject):
    """
    Represents a super bullet falling from the top of the screen.
    """

    def __init__(self):
        super().__init__("pictures/super_bullet.png")
