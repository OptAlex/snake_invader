import pyglet
from pyglet.window import mouse

from Classes.snake import Snake
from Classes.food import Food, SuperFood
from Classes.falling_objects import Bullet, Heart, SuperBullet
from Classes.lifes import Lifes
from help_functions.const import WINDOW_WIDTH, WINDOW_HEIGHT

import random
from help_functions.ui import init_ui_elements

start_screen = True
game_over_screen = False
batch = pyglet.graphics.Batch()

# Declare the base chance for bullet and super bullet
bullet_gen_base_chance = 0.004
super_bullet_gen_base_chance = 0.00025


# Initialize UI elements
(
    play_button,
    play_text,
    restart_button,
    restart_text,
    score_label,
    heart_sprite,
    heart_info_text,
    super_bullet_sprite,
    super_bullet_info_text,
    bullet_sprite,
    bullet_info_text,
    snake_sprite,
    snake_info_text,
    image_sprite,
    food_sprite,
    food_info_text,
    super_food_sprite,
    super_food_info_text,
    high_score_display,
) = init_ui_elements(batch)


# Initialize Pyglet window
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

# Create instances of the Snake, Food, SuperFood, and Lifes classes
snake = Snake()
food = Food(snake)
super_food = SuperFood(snake)
lifes = Lifes(snake)

objects = []
score_label = pyglet.text.Label("Score: 0", font_size=20, x=10, y=WINDOW_HEIGHT - 30)
paused = False
high_score_labels = []


def update_score_label():
    """
    Updates the score label with the current score.
    """
    score_label.text = f"Score: {snake.score}"


def restart_game():
    global snake, food, super_food, lifes, objects, score_label, high_score_labels
    snake = Snake()
    food = Food(snake)
    super_food = SuperFood(snake)
    lifes = Lifes(snake)
    objects = []
    score_label.text = "Score: 0"


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
    global high_score_labels
    window.clear()
    if high_score_labels is None:
        high_score_labels = []

    if start_screen:
        image_sprite.draw()
        play_button.draw()
        play_text.draw()
        heart_sprite.draw()
        heart_info_text.draw()
        super_bullet_sprite.draw()
        super_bullet_info_text.draw()
        bullet_sprite.draw()
        bullet_info_text.draw()
        snake_sprite.draw()
        snake_info_text.draw()
        food_sprite.draw()
        food_info_text.draw()
        super_food_sprite.draw()
        super_food_info_text.draw()
    elif game_over_screen:
        score_label.text = f"Score: {snake.score}"
        score_label.draw()
        restart_button.draw()
        restart_text.draw()

        # Shift high scores and draw them
        third_height = WINDOW_HEIGHT // 3
        for i, high_score_label in enumerate(high_score_display.high_score_labels):
            high_score_label.y = (
                third_height + 70 + i * 30
            )
            high_score_label.draw()

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
        if (
            start_screen
            and play_button.x <= x <= play_button.x + play_button.width
            and play_button.y <= y <= play_button.y + play_button.height
        ):
            # Clicked Play button
            start_screen = False
        elif (
            game_over_screen
            and restart_button.x <= x <= restart_button.x + restart_button.width
            and restart_button.y <= y <= restart_button.y + restart_button.height
        ):
            # Clicked Restart button
            game_over_screen = False
            restart_game()

def update(dt):
    global objects, paused, game_over_screen, start_screen, high_score_display

    if paused or game_over_screen or start_screen:
        return

    snake.move()

    if snake.collides_with_food(food):
        food.eat()
        snake.grow(1)
        snake.score += 1
        if random.random() < 0.05:
            super_food.position = super_food.generate_position()

    elif snake.collides_with_food(super_food):
        super_food.eat()
        snake.grow(5)
        snake.score += 5

    for obj in objects[:]:  # Loop over a copy of the list as we'll modify it
        obj.move()
        if snake.collides_with_object(obj):
            if isinstance(obj, Bullet):  # If the object is a bullet, decrease life
                snake.lose_life()
            elif isinstance(obj, Heart):  # If the object is a heart, increase life
                if snake.lives < 5:
                    snake.lives += 1
            elif isinstance(
                obj, SuperBullet
            ):
                for _ in range(3):  # Lose life 3 times
                    snake.lose_life()
            objects.remove(obj)

    objects = [obj for obj in objects if not obj.is_off_screen()]

    bullet_gen_chance = bullet_gen_base_chance
    super_bullet_gen_chance = super_bullet_gen_base_chance

    if snake.score >= 7:
        difficulty_factor = 1 + ((snake.score - 7) // 7)
        bullet_gen_chance += difficulty_factor * 0.0015
        super_bullet_gen_chance += difficulty_factor * 0.0003

    # Generate Bullets, Super Bullets, and Hearts based on the updated chances
    if random.random() < bullet_gen_chance:
        objects.append(Bullet())
    if random.random() < super_bullet_gen_chance:
        objects.append(SuperBullet())
    if random.random() < 0.0005:
        objects.append(Heart())
    if random.randint(0, 1000) == 1:
        super_food.position = super_food.generate_position()

    if snake.collides_with_self() or snake.lives <= 0:
        with open("highscores.txt", "a") as f:
            f.write(f"{snake.score}\n")
        high_score_display.update()
        game_over_screen = True
        return

    update_score_label()

pyglet.clock.schedule_interval(update, 1 / 90)

pyglet.app.run()