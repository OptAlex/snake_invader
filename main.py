import pyglet
from pyglet.window import mouse

from Classes.snake import Snake
from Classes.food import Food, SuperFood
from Classes.falling_objects import Bullet, Heart  # import Heart class here
from Classes.lifes import Lifes
from help_functions.const import WINDOW_WIDTH, WINDOW_HEIGHT, MOVE_DICT

import random
from help_functions.ui import init_ui_elements

start_screen = True
game_over_screen = False
batch = pyglet.graphics.Batch()


play_button, play_text, restart_button, restart_text, score_text, image_sprite = init_ui_elements(batch)


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

def restart_game():
    global snake, food, super_food, lifes, objects, score_label
    snake = Snake()
    food = Food(snake)
    super_food = SuperFood(snake)
    lifes = Lifes(snake)
    objects = []
    score_label.text = 'Score: 0'

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
    if start_screen:
        image_sprite.draw()
        play_button.draw()
        play_text.draw()
    elif game_over_screen:
        score_text.text = f'Score: {snake.score}'
        score_text.draw()
        restart_button.draw()
        restart_text.draw()
    else:
        # Draw the game
        snake.draw()
        food.draw()
        super_food.draw()
        lifes.draw()
        for obj in objects:
            obj.draw()
        score_label.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    global start_screen, game_over_screen
    if button == mouse.LEFT:
        if start_screen and play_button.x <= x <= play_button.x + play_button.width \
                and play_button.y <= y <= play_button.y + play_button.height:
            # Clicked Play button
            start_screen = False
        elif game_over_screen and restart_button.x <= x <= restart_button.x + restart_button.width \
                and restart_button.y <= y <= restart_button.y + restart_button.height:
            # Clicked Restart button
            game_over_screen = False
            restart_game()


def update(dt):
    global objects, paused, game_over_screen, start_screen

    if paused or game_over_screen or start_screen:
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
        game_over_screen = True
        return

    if random.randint(0, 500) == 1:
        super_food.position = super_food.generate_position()

    update_score_label()


pyglet.clock.schedule_interval(update, 1 / 10)

pyglet.app.run()
