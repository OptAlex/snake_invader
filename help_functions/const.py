# Constants defining game parameters

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

SEGMENT_SIZE = 20  # The size of each snake segment
SEGMENT_SPEED = 20  # The speed of the snake
BULLET_SPEED = 3

# Directions as string constants
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
UP_RIGHT = "up_right"
DOWN_RIGHT = "down_right"
UP_LEFT = "up_left"
DOWN_LEFT = "down_left"

# Dictionary mapping directions to rotations in degrees
ROTATIONS = {
    RIGHT: -90,
    LEFT: 90,
    UP: 180,
    DOWN: 0,
}

# Dictionary mapping curve directions to rotations in degrees
CURVES = {
    UP_RIGHT: 0,
    DOWN_RIGHT: 270,
    UP_LEFT: 90,
    DOWN_LEFT: 180,
}

# Dictionary mapping directions to movement in terms of (x, y) coordinates
MOVE_DICT = {
    UP: (0, SEGMENT_SPEED),
    DOWN: (0, -SEGMENT_SPEED),
    LEFT: (-SEGMENT_SPEED, 0),
    RIGHT: (SEGMENT_SPEED, 0),
}
