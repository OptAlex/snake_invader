# Set up the dimensions of the game window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Set up the dimensions and speed of each segment of the snake_invaders
SEGMENT_SIZE = 20
SEGMENT_SPEED = 20
BULLET_SPEED = 3

# Set up the colors

FOOD_COLOR = (255, 174, 0)
SUPER_FOOD_COLOR = (128, 0, 128)

# Directions
UP_RIGHT = "up_right"
DOWN_RIGHT = "down_right"
UP_LEFT = "up_left"
DOWN_LEFT = "down_left"

ROTATIONS = {
        "right": -90,
        "left": 90,
        "up": 180,
        "down": 0,
    }

CURVES = {
    UP_RIGHT: 0,
    DOWN_RIGHT: 270,
    UP_LEFT: 90,
    DOWN_LEFT: 180,
}

MOVE_DICT = {
    "up": (0, SEGMENT_SPEED),
    "down": (0, -SEGMENT_SPEED),
    "left": (-SEGMENT_SPEED, 0),
    "right": (SEGMENT_SPEED, 0),
}