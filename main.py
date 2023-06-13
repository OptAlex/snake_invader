import pyglet
from Classes.snake import Snake
from Classes.food import Food, SuperFood
from Classes.falling_objects import Bullet, Heart  # import Heart class here
from Classes.lifes import Lifes
from help_functions.const import WINDOW_WIDTH, WINDOW_HEIGHT, MOVE_DICT
import random

# Initialize Pyglet window
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

# Create instances of the Snake, Food, SuperFood, and Lifes classes
snake = Snake()
food = Food(snake)
super_food = SuperFood(snake)
lifes = Lifes(snake)

objects = []
score_label = pyglet.text.Label('Score: 0', font_size=20, x=10, y=WINDOW_HEIGHT-30)
paused = False

def update_score_label():
    """
    Updates the score label with the current score.
    """
    score_label.text = f'Score: {snake.score}'

@window.event
def on_key_press(symbol, modifiers):
    global paused
    if symbol == pyglet.window.key.UP:
        snake.change_direction("up")
    elif symbol == pyglet.window.key.DOWN:
        snake.change_direction("down")
    elif symbol == pyglet.window.key.LEFT:
        snake.change_direction("left")
    elif symbol == pyglet.window.key.RIGHT:
        snake.change_direction("right")
    elif symbol == pyglet.window.key.P:
        paused = not paused

@window.event
def on_draw():
    window.clear()
    snake.draw()
    food.draw()
    super_food.draw()
    lifes.draw()
    for obj in objects:
        obj.draw()
    update_score_label()
    score_label.draw()

def update(dt):
    global objects, paused

    if paused:
        return

    snake.move()

    if snake.collides_with_food(food):
        food.eat()
        snake.score += 1
        dx, dy = MOVE_DICT[snake.direction]
        last_segment = snake.segments[-1]
        new_segment = (last_segment[0] - dx, last_segment[1] - dy)
        snake.segments.append(new_segment)
        if random.random() < 0.1:
            super_food.position = super_food.generate_position()

    elif snake.collides_with_food(super_food):
        super_food.eat()
        snake.score += 5
        dx, dy = MOVE_DICT[snake.direction]
        last_segment = snake.segments[-1]
        for _ in range(5):
            new_segment = (last_segment[0] - dx, last_segment[1] - dy)
            snake.segments.append(new_segment)

    for obj in objects[:]:  # Loop over a copy of the list as we'll modify it
        obj.move()
        if snake.collides_with_object(obj):
            if isinstance(obj, Bullet):  # If the object is a bullet, decrease life
                snake.lose_life()
            elif isinstance(obj, Heart):  # If the object is a heart, increase life
                if snake.lives < 5:
                    snake.lives += 1
            objects.remove(obj)

    objects = [obj for obj in objects if not obj.is_off_screen()]

    if random.random() < 0.02:
        objects.append(Bullet())
    if random.random() < 0.01:  # Adjust this value to modify the frequency of hearts
        objects.append(Heart())

    if snake.collides_with_self() or snake.lives <= 0:
        pyglet.app.exit()

    if random.randint(0, 500) == 1:
        super_food.position = super_food.generate_position()

    update_score_label()

pyglet.clock.schedule_interval(update, 1 / 10)

pyglet.app.run()
