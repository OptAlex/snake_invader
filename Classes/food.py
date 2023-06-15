import random
import pyglet
from abc import ABC, abstractmethod
from help_functions.const import WINDOW_WIDTH, SEGMENT_SIZE, WINDOW_HEIGHT
from help_functions.image import load_image


class AbstractFood(ABC):
    """
    Abstract base class for all types of food.
    """

    def __init__(self, snake):
        """
        Initialize an AbstractFood instance.

        Args:
            snake: The snake instance that the food interacts with.
        """
        self.snake = snake
        self.position = self.generate_position()
        self.sprite = None

    def generate_position(self):
        """
        Generate a new random position for the food that is not occupied by the snake.
        The position aligns with the snake's movement.

        Returns:
            A tuple (x, y) representing the new position of the food.
        """
        while True:
            x = (
                random.randint(0, (WINDOW_WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE)
                * SEGMENT_SIZE
            )
            y = (
                random.randint(1, (WINDOW_HEIGHT - SEGMENT_SIZE) // SEGMENT_SIZE)
                * SEGMENT_SIZE
            )

            if (x, y) not in self.snake.segments:
                return x, y

    def draw(self):
        """
        Draw the food on the screen at its current position.
        """
        if self.position is not None and self.sprite:
            self.sprite.x, self.sprite.y = (
                self.position[0] + SEGMENT_SIZE // 2,
                self.position[1] + SEGMENT_SIZE // 2,
            )
            self.sprite.draw()

    @abstractmethod
    def eat(self):
        """
        Regenerate the position of the food when it's eaten.
        """
        self.position = self.generate_position()


class Food(AbstractFood):
    """
    Represents normal food.
    """

    def __init__(self, snake):
        super().__init__(snake)
        self.sprite = pyglet.sprite.Sprite(load_image("pictures/food.png"))

    def eat(self):
        super().eat()


class SuperFood(AbstractFood):
    """
    Represents super food.
    """

    def __init__(self, snake):
        super().__init__(snake)
        self.sprite = pyglet.sprite.Sprite(load_image("pictures/super_food.png"))

    def eat(self):
        """
        Hide the super food when it's eaten.
        """
        self.position = None
