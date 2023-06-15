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
    UP,
    LEFT,
    DOWN,
    RIGHT,
)
from help_functions.image import load_image
import random


class Snake:
    """
    Represents the snake_invaders in the game. The snake_invaders is composed of segments and can move, change direction,
    and collide with food, itself, walls, bullets, and other falling objects.
    """

    def __init__(self):
        self.segments = [
            (
                random.randint(0, WINDOW_WIDTH // SEGMENT_SIZE - 1) * SEGMENT_SIZE,
                random.randint(0, WINDOW_HEIGHT // SEGMENT_SIZE - 1) * SEGMENT_SIZE,
            )
        ]
        self.direction = UP
        self.lives = 3
        self.head_image = load_image("pictures/snake_head.png")
        self.middle_image = load_image("pictures/snake_middle.png")
        self.tail_image = load_image("pictures/snake_tail.png")
        self.middle_right_up_image = load_image("pictures/snake_up_right.png")
        self.head_sprite = pyglet.sprite.Sprite(self.head_image)
        self.score = 0
        self.move_counter = 0
        self.growth_due = 0

    def move(self):
        """
        Moves the snake in the current direction. The snake moves once every 5 frames, and can wrap around the screen.
        If the snake is not due to grow, the last segment is removed after moving.
        """
        self.move_counter += 1
        if self.move_counter < 4:  # Only move the snake once every 4 frames
            return
        self.move_counter = 0

        x, y = self.segments[0]
        dx, dy = MOVE_DICT[self.direction]
        x += dx
        y += dy
        if x < 0:
            x = WINDOW_WIDTH - SEGMENT_SIZE
        elif x >= WINDOW_WIDTH:
            x = 0
        if y < 0:
            y = WINDOW_HEIGHT - SEGMENT_SIZE
        elif y >= WINDOW_HEIGHT:
            y = 0
        self.segments.insert(0, (x, y))
        if self.growth_due > 0:  # Check if the snake is due to grow
            self.growth_due -= 1  # If so, decrement growth_due
        else:
            self.segments.pop()  # If not, remove the last segment

    def get_direction(self, segment1, segment2):
        """
        Calculates the direction from segment1 to segment2.

        Args:
            segment1: The starting segment (a tuple of x and y coordinates)
            segment2: The destination segment (a tuple of x and y coordinates)

        Returns:
            The direction from segment1 to segment2 as a string ('UP', 'DOWN', 'LEFT', 'RIGHT').
        """
        x1, y1 = segment1
        x2, y2 = segment2
        if abs(x1 - x2) == WINDOW_WIDTH - SEGMENT_SIZE:  # If segments at opposite edges
            if x1 < x2:
                return LEFT
            else:
                return RIGHT
        elif x1 < x2:
            return RIGHT
        elif x1 > x2:
            return LEFT
        elif y1 < y2:
            return UP
        else:
            return DOWN

    def lose_life(self):
        """
        Decreases the snake's lives by 1, if the snake has more than 0 lives.
        """
        if self.lives > 0:
            self.lives -= 1

    def change_direction(self, new_direction):
        """
        Changes the direction of the snake if the new direction is not the opposite of the current direction.

        Args:
            new_direction: The new direction for the snake as a string ('UP', 'DOWN', 'LEFT', 'RIGHT').
        """
        if new_direction in [UP, DOWN, LEFT, RIGHT]:
            if new_direction == UP and self.direction != DOWN:
                self.direction = UP
            elif new_direction == DOWN and self.direction != UP:
                self.direction = DOWN
            elif new_direction == LEFT and self.direction != RIGHT:
                self.direction = LEFT
            elif new_direction == RIGHT and self.direction != LEFT:
                self.direction = RIGHT

    def get_curve(self, i):
        """
        Calculates the curve direction between three consecutive segments.

        Args:
            i: The index of the middle segment in the segments list.

        Returns:
            The curve direction as a string ('UP_RIGHT', 'UP_LEFT', 'DOWN_RIGHT', 'DOWN_LEFT') or None if no curve.
        """
        prev_direction = self.get_direction(self.segments[i - 1], self.segments[i])
        next_direction = self.get_direction(self.segments[i], self.segments[i + 1])
        if prev_direction == UP and next_direction == RIGHT:
            return UP_RIGHT
        elif prev_direction == UP and next_direction == LEFT:
            return UP_LEFT
        elif prev_direction == DOWN and next_direction == RIGHT:
            return DOWN_RIGHT
        elif prev_direction == DOWN and next_direction == LEFT:
            return DOWN_LEFT
        elif prev_direction == RIGHT and next_direction == DOWN:
            return UP_LEFT
        elif prev_direction == RIGHT and next_direction == UP:
            return DOWN_LEFT
        elif prev_direction == LEFT and next_direction == UP:
            return DOWN_RIGHT
        elif prev_direction == LEFT and next_direction == DOWN:
            return UP_RIGHT
        else:
            return None

    def draw(self):
        """
        Draws the snake on the screen. The head, body, and tail of the snake are drawn separately, and the body includes curves if the snake turns.
        """
        self.head_sprite.rotation = ROTATIONS.get(self.direction, None)
        self.head_sprite.x, self.head_sprite.y = (
            self.segments[0][0] + SEGMENT_SIZE // 2,
            self.segments[0][1] + SEGMENT_SIZE // 2,
        )
        self.head_sprite.draw()
        if len(self.segments) > 1:
            tail_direction = self.get_direction(self.segments[-2], self.segments[-1])
            tail_sprite = pyglet.sprite.Sprite(self.tail_image)
            tail_sprite.rotation = ROTATIONS.get(tail_direction, None)
            tail_sprite.x, tail_sprite.y = (
                self.segments[-1][0] + SEGMENT_SIZE // 2,
                self.segments[-1][1] + SEGMENT_SIZE // 2,
            )
            tail_sprite.draw()
        for i in range(1, len(self.segments) - 1):
            segment = self.segments[i]
            curve = self.get_curve(i)
            if curve:
                middle_image = self.middle_right_up_image
                rotation = CURVES.get(curve, None)
            else:
                middle_image = self.middle_image
                middle_direction = self.get_direction(
                    self.segments[i - 1], self.segments[i + 1]
                )
                rotation = ROTATIONS.get(middle_direction, None)
            middle_sprite = pyglet.sprite.Sprite(middle_image)
            middle_sprite.rotation = rotation
            middle_sprite.x, middle_sprite.y = (
                segment[0] + SEGMENT_SIZE // 2,
                segment[1] + SEGMENT_SIZE // 2,
            )
            middle_sprite.draw()

    def grow(self, segments):
        """
        Increases the length of the snake by a specified number of segments.

        Args:
            segments: The number of segments to add to the snake.
        """

        self.growth_due += segments
        dx, dy = MOVE_DICT[self.direction]
        last_segment = self.segments[-1]
        for _ in range(segments):
            new_segment = (last_segment[0] - dx, last_segment[1] - dy)
            self.segments.append(new_segment)

    def collides_with_food(self, food):
        """
        Checks if the snake's head collides with the food.

        Args:
            food: The food object.

        Returns:
            True if the snake's head and the food are close enough to collide, False otherwise.
        """
        if food.position is None:
            return False
        head_x, head_y = self.segments[0]
        food_x, food_y = food.position
        return (
            abs(head_x - food_x) < SEGMENT_SIZE * 1.5
            and abs(head_y - food_y) < SEGMENT_SIZE * 1.5
        )

    def collides_with_self(self):
        """
        Checks if the snake's head collides with its body.

        Returns:
            True if the snake's head collides with its body, False otherwise.
        """
        return self.segments[0] in self.segments[1:-1]

    def collides_with_wall(self):
        """
        Checks if the snake's head collides with the wall.

        Returns:
            True if the snake's head collides with the wall, False otherwise.
        """

        x, y = self.segments[0]
        return x < 0 or x >= WINDOW_WIDTH or y < 0 or y >= WINDOW_HEIGHT

    def collides_with_bullet(self, bullet):
        """
        Checks if the snake's head collides with a bullet.

        Args:
            bullet: The bullet object.

        Returns:
            True if the snake's head collides with the bullet, False otherwise.
        """
        head_x, head_y = self.segments[0]
        bullet_x, bullet_y = bullet.sprite.x, bullet.sprite.y
        return (
            abs(head_x - bullet_x) <= SEGMENT_SIZE / 2
            and abs(head_y - bullet_y) <= SEGMENT_SIZE / 2
        )

    def collides_with_object(self, obj):
        """
        Checks if the snake's head collides with a given object.

        Args:
            obj: The object to check for collision with.

        Returns:
            True if the snake's head collides with the object, False otherwise.
        """
        head_x, head_y = self.segments[0]
        obj_x, obj_y = obj.sprite.x, obj.sprite.y
        return (
            abs(head_x - obj_x) <= SEGMENT_SIZE and abs(head_y - obj_y) <= SEGMENT_SIZE
        )
