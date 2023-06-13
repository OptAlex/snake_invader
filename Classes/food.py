import random
import pyglet
from abc import ABC, abstractmethod
from help_functions.const import WINDOW_WIDTH, SEGMENT_SIZE, WINDOW_HEIGHT
from help_functions.image import load_image


class AbstractFood(ABC):
    def __init__(self, snake):
        self.snake = snake  # Add a reference to the snake
        self.position = self.generate_position()
        self.sprite = None  # Will be set in the child classes


    def snake_occupies_position(self, position):
        """Check if the snake occupies a certain position."""
        return position in self.snake.segments

    def generate_position(self):
        """
        Generates a new random position for the food. The position is always a multiple
        of SEGMENT_SIZE, so it aligns with the snake_invaders's movement.

        Returns:
            tuple: A tuple (x, y) representing the position of the food.
        """
        while True:
            # Calculate random x and y coordinates that are multiples of SEGMENT_SIZE
            x = random.randint(0, (WINDOW_WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
            # Exclude the first row by starting from 1 instead of 0
            y = random.randint(1, (WINDOW_HEIGHT - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE

            # If the new position is not on the snake, return it
            if (x, y) not in self.snake.segments:
                return x, y

    def draw(self):
        if self.sprite:
            self.sprite.x, self.sprite.y = self.position[0] + SEGMENT_SIZE // 2, self.position[1] + SEGMENT_SIZE // 2
            self.sprite.draw()

    @abstractmethod
    def eat(self):
        """
        Regenerates the position of the food when it's eaten.
        """
        self.position = self.generate_position()


class Food(AbstractFood):
    def __init__(self, snake):
        super().__init__(snake)
        self.sprite = pyglet.sprite.Sprite(load_image('pictures/food.png'))

    def generate_position(self):
        return super().generate_position()

    def draw(self):
        super().draw()

    def eat(self):
        super().eat()


class SuperFood(AbstractFood):
    def __init__(self, snake):
        super().__init__(snake)
        self.sprite = pyglet.sprite.Sprite(load_image('pictures/super_food.png'))

    def generate_position(self):
        return super().generate_position()

    def draw(self):
        if self.position:
            super().draw()

    def eat(self):
        self.position = None
