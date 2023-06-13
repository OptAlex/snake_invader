import pyglet
from pyglet import shapes, text
from help_functions.const import WINDOW_WIDTH, WINDOW_HEIGHT
from help_functions.image import load_image


def compute_and_center_sprite_text(image, info_text, y_pos, padding):
    combined_width = image.width + padding + info_text.content_width
    start_pos = (WINDOW_WIDTH - combined_width) // 2
    sprite = pyglet.sprite.Sprite(image, x=start_pos, y=y_pos)
    info_text.x = sprite.x + image.width + padding
    return sprite, info_text


def init_ui_elements(batch):
    third_height = WINDOW_HEIGHT // 3
    padding = 10

    shift_up = (
        45  # change this value to adjust the vertical shift for the existing elements
    )

    high_score_display = HighScoreDisplay(batch)

    play_button = shapes.Rectangle(
        WINDOW_WIDTH // 2 - 50,
        third_height + 70 + shift_up,
        100,
        50,
        color=(129, 180, 69),
        batch=batch,
    )
    play_text = text.Label(
        "Play",
        font_name="Verdana",
        font_size=20,
        x=WINDOW_WIDTH // 2,
        y=third_height + 95 + shift_up,
        anchor_x="center",
        anchor_y="center",
        batch=batch,
    )

    restart_button = shapes.Rectangle(
        WINDOW_WIDTH // 2 - 50,
        third_height - 50,
        100,
        50,
        color=(211, 122, 105),
        batch=batch,
    )
    restart_text = text.Label(
        "Restart",
        font_name="Verdana",
        font_size=20,
        x=WINDOW_WIDTH // 2,
        y=third_height - 25,
        anchor_x="center",
        anchor_y="center",
        batch=batch,
    )

    score_text = text.Label(
        "",
        font_name="Verdana",
        font_size=20,
        x=WINDOW_WIDTH // 2,
        y=third_height + 250 + shift_up,
        anchor_x="center",
        anchor_y="center",
        batch=batch,
    )

    # Added Images and Texts
    food_info_text = text.Label(
        "gain +1.",
        font_name="Verdana",
        font_size=15,
        y=third_height + 35 + shift_up,
        anchor_x="left",
        anchor_y="center",
        batch=batch,
    )
    food_image = load_image("pictures/food.png")
    food_sprite, food_info_text = compute_and_center_sprite_text(
        food_image, food_info_text, third_height + 35 + shift_up, padding
    )

    super_food_info_text = text.Label(
        "gain +5.",
        font_name="Verdana",
        font_size=15,
        y=third_height - 15 + shift_up,
        anchor_x="left",
        anchor_y="center",
        batch=batch,
    )
    super_food_image = load_image("pictures/super_food.png")
    super_food_sprite, super_food_info_text = compute_and_center_sprite_text(
        super_food_image, super_food_info_text, third_height - 15 + shift_up, padding
    )

    # Original Images and Texts now shifted downwards
    heart_info_text = text.Label(
        "increase your lives by one.",
        font_name="Verdana",
        font_size=15,
        y=third_height - 65 + shift_up,
        anchor_x="left",
        anchor_y="center",
        batch=batch,
    )
    heart_image = load_image("pictures/heart.png")
    heart_sprite, heart_info_text = compute_and_center_sprite_text(
        heart_image, heart_info_text, third_height - 65 + shift_up, padding
    )

    super_bullet_info_text = text.Label(
        "delete three lives at once.",
        font_name="Verdana",
        font_size=15,
        y=third_height - 115 + shift_up,
        anchor_x="left",
        anchor_y="center",
        batch=batch,
    )
    super_bullet_image = load_image("pictures/super_bullet.png")
    super_bullet_sprite, super_bullet_info_text = compute_and_center_sprite_text(
        super_bullet_image,
        super_bullet_info_text,
        third_height - 115 + shift_up,
        padding,
    )

    bullet_info_text = text.Label(
        "decrease your lives by one.",
        font_name="Verdana",
        font_size=15,
        y=third_height - 165 + shift_up,
        anchor_x="left",
        anchor_y="center",
        batch=batch,
    )
    bullet_image = load_image("pictures/bullet.png")
    bullet_sprite, bullet_info_text = compute_and_center_sprite_text(
        bullet_image, bullet_info_text, third_height - 165 + shift_up, padding
    )

    snake_info_text = text.Label(
        "If the snake hits itself, you lose.",
        font_name="Verdana",
        font_size=15,
        y=third_height - 215 + shift_up,
        anchor_x="left",
        anchor_y="center",
        batch=batch,
    )
    snake_image = load_image("pictures/explosion.png")
    snake_sprite, snake_info_text = compute_and_center_sprite_text(
        snake_image, snake_info_text, third_height - 215 + shift_up, padding
    )

    image = load_image("pictures/snake_ui.png")
    image_sprite = pyglet.sprite.Sprite(
        image, x=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2 + 140 + shift_up, batch=batch
    )

    return (
        play_button,
        play_text,
        restart_button,
        restart_text,
        score_text,
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
    )


class HighScoreDisplay:
    def __init__(self, batch=None, y_shift=0):
        self.high_score_labels = [
            pyglet.text.Label(
                "",
                font_name="Verdana",
                font_size=20,
                x=WINDOW_WIDTH // 2,
                y=y_shift + i * 30,
                anchor_x="center",
                anchor_y="center",
                batch=batch,
            )
            for i in range(3)
        ]
        self.update()

    def get_high_scores(self):
        try:
            with open("highscores.txt", "r") as f:
                scores = f.read().split("\n")
            scores = [int(score) for score in scores if score]
            scores.sort(reverse=True)
            return scores[:3]
        except FileNotFoundError:
            return []

    def update(self):
        high_scores = self.get_high_scores()
        for i, score in enumerate(
            high_scores[::-1]
        ):  # Enumerate over reversed high_scores
            self.high_score_labels[
                i
            ].text = (
                f"High Score {3 - i}: {score}"  # 3 - i to reverse the order of labels
            )