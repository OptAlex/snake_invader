import pyglet
from help_functions.const import (
    SEGMENT_SIZE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    DOWN_RIGHT,
    DOWN_LEFT,
    UP_LEFT,
    UP_RIGHT,
    MOVE_DICT,
    ROTATIONS,
    CURVES,
)
from help_functions.image import load_image
import random

class Snake:
    """
    Represents the snake_invaders in the game. The snake_invaders is composed of segments and can move, change direction, and collide with food or itself.
    """

    def __init__(self):
        self.segments = [(random.randint(0, WINDOW_WIDTH//SEGMENT_SIZE - 1)*SEGMENT_SIZE,
                          random.randint(0, WINDOW_HEIGHT//SEGMENT_SIZE - 1)*SEGMENT_SIZE)]
        self.direction = "up"
        self.lives = 3

        self.head_image = load_image('pictures/snake_head.png')
        self.middle_image = load_image('pictures/snake_middle.png')
        self.tail_image = load_image('pictures/snake_tail.png')
        self.middle_right_up_image = load_image('pictures/snake_up_right.png')

        self.head_sprite = pyglet.sprite.Sprite(self.head_image)
        self.middle_sprites = [pyglet.sprite.Sprite(self.middle_image) for _ in range(len(self.segments) - 2)]
        self.tail_sprite = pyglet.sprite.Sprite(self.tail_image)
        self.score = 0

    def get_direction(self, segment1, segment2):
        x1, y1 = segment1
        x2, y2 = segment2
        if x1 < x2:
            return "right"
        elif x1 > x2:
            return "left"
        elif y1 < y2:
            return "up"
        else:
            return "down"

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    def move(self):
        x, y = self.segments[0]

        dx, dy = MOVE_DICT[self.direction]

        x += dx
        y += dy

        # Wrap around if snake_invaders goes off screen
        if x < 0:
            x = WINDOW_WIDTH - SEGMENT_SIZE
        elif x >= WINDOW_WIDTH:
            x = 0
        if y < 0:
            y = WINDOW_HEIGHT - SEGMENT_SIZE
        elif y >= WINDOW_HEIGHT:
            y = 0

        self.segments.insert(0, (x, y))
        self.segments.pop()

    def change_direction(self, new_direction):
        """
        Changes the direction of the snake_invaders to the new direction, unless it is the opposite of the current direction.

        Args:
            new_direction (str): The new direction for the snake_invaders, should be "up", "down", "left", or "right".
        """
        if new_direction in ["up", "down", "left", "right"]:
            if new_direction == "up" and self.direction != "down":
                self.direction = "up"
            elif new_direction == "down" and self.direction != "up":
                self.direction = "down"
            elif new_direction == "left" and self.direction != "right":
                self.direction = "left"
            elif new_direction == "right" and self.direction != "left":
                self.direction = "right"

    def get_curve(self, i):
        """
        Get the type of curve at the i-th segment.

        Args:
            i (int): Index of the segment in the self.segments list.

        Returns:
            str: The type of curve, can be UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT, or None.
        """
        prev_direction = self.get_direction(self.segments[i - 1], self.segments[i])
        next_direction = self.get_direction(self.segments[i], self.segments[i + 1])

        if prev_direction == "up" and next_direction == "right":
            return UP_RIGHT
        elif prev_direction == "up" and next_direction == "left":
            return UP_LEFT
        elif prev_direction == "down" and next_direction == "right":
            return DOWN_RIGHT
        elif prev_direction == "down" and next_direction == "left":
            return DOWN_LEFT
        elif prev_direction == "right" and next_direction == "down":
            return UP_LEFT
        elif prev_direction == "right" and next_direction == "up":
            return DOWN_LEFT
        elif prev_direction == "left" and next_direction == "up":
            return DOWN_RIGHT
        elif prev_direction == "left" and next_direction == "down":
            return UP_RIGHT
        else:
            return None

    def draw(self):
        """
        Draws each segment of the snake_invaders on the window.
        """

        self.head_sprite.rotation = ROTATIONS.get(self.direction, None)

        # Adjust for the center of the sprite
        self.head_sprite.x, self.head_sprite.y = self.segments[0][0] + SEGMENT_SIZE // 2, self.segments[0][
            1] + SEGMENT_SIZE // 2
        self.head_sprite.draw()

        # Draw the tail of the snake
        if len(self.segments) > 1:
            tail_direction = self.get_direction(self.segments[-2], self.segments[-1])
            tail_sprite = pyglet.sprite.Sprite(self.tail_image)
            tail_sprite.rotation = ROTATIONS.get(tail_direction, None)

            # Adjust for the center of the sprite
            tail_sprite.x, tail_sprite.y = self.segments[-1][0] + SEGMENT_SIZE // 2, self.segments[-1][
                1] + SEGMENT_SIZE // 2
            tail_sprite.draw()

        # Draw the middle parts of the snake
        for i in range(1, len(self.segments) - 1):
            segment = self.segments[i]
            curve = self.get_curve(i)

            if curve:  # Draw a curve segment if needed
                middle_image = load_image('pictures/snake_up_right.png')
                rotation = CURVES.get(curve, None)
            else:  # Draw a regular segment
                middle_image = self.middle_image
                middle_direction = self.get_direction(self.segments[i - 1], self.segments[i + 1])
                rotation = ROTATIONS.get(middle_direction, None)

            middle_sprite = pyglet.sprite.Sprite(middle_image)
            middle_sprite.rotation = rotation

            # Adjust for the center of the sprite
            middle_sprite.x, middle_sprite.y = segment[0] + SEGMENT_SIZE // 2, segment[1] + SEGMENT_SIZE // 2
            middle_sprite.draw()

    def collides_with_food(self, food):
        """
        Checks if the snake_invaders's head has collided with the food.

        Args:
            food (Food): The food object.

        Returns:
            bool: True if the snake_invaders's head and the food are at the same position, False otherwise.
        """
        if food.position is None:
            return False
        return self.segments[0] == food.position

    def collides_with_self(self):
        """
        Checks if the snake's head has collided with its body.

        Returns:
            bool: True if the snake's head is in the same position as any of its other segments, False otherwise.
        """
        return self.segments[0] in self.segments[1:]

    def collides_with_wall(self):
        """
        Checks if the snake_invaders's head has collided with the wall.

        Returns:
            bool: True if the snake_invaders's head is outside the window bounds, False otherwise.
        """
        x, y = self.segments[0]
        return x < 0 or x >= WINDOW_WIDTH or y < 0 or y >= WINDOW_HEIGHT

    def collides_with_bullet(self, bullet):
        head_x, head_y = self.segments[0]
        bullet_x, bullet_y = bullet.sprite.x, bullet.sprite.y
        return abs(head_x - bullet_x) <= SEGMENT_SIZE / 2 and abs(head_y - bullet_y) <= SEGMENT_SIZE / 2

    def collides_with_object(self, obj):
        """
        Checks if the snake's head has collided with a falling object.

        Args:
            obj (FallingObject): The falling object to check collision with.

        Returns:
            bool: True if the snake's head and the falling object are at the same position, False otherwise.
        """
        head_x, head_y = self.segments[0]
        obj_x, obj_y = obj.sprite.x, obj.sprite.y
        return abs(head_x - obj_x) <= SEGMENT_SIZE / 2 and abs(head_y - obj_y) <= SEGMENT_SIZE / 2


