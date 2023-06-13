import pyglet
from help_functions.const import WINDOW_WIDTH, WINDOW_HEIGHT

class Lifes:
    def __init__(self, snake):
        self.snake = snake
        self.heart_image = pyglet.image.load('pictures/heart.png')  # Replace with the path to your heart image

    def draw(self):
        for i in range(self.snake.lives):
            heart_sprite = pyglet.sprite.Sprite(self.heart_image, x=WINDOW_WIDTH - 20 * (i+1), y=WINDOW_HEIGHT - 20)
            heart_sprite.draw()
