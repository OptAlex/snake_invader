import pyglet
from pyglet import shapes, text
from help_functions.const import WINDOW_WIDTH, WINDOW_HEIGHT
from help_functions.image import load_image


def init_ui_elements(batch):
    """
    Initializes UI elements such as buttons and labels, and adds them to the given batch.

    Args:
        batch (pyglet.graphics.Batch): The batch that all UI elements are added to.

    Returns:
        tuple: A tuple containing all initialized UI elements.
    """

    third_height = WINDOW_HEIGHT // 3

    play_button = shapes.Rectangle(
        WINDOW_WIDTH // 2 - 50, third_height, 100, 50, color=(129, 180, 69), batch=batch
    )
    play_text = text.Label(
        "Play",
        font_size=20,
        x=WINDOW_WIDTH // 2,
        y=third_height + 25,
        anchor_x="center",
        anchor_y="center",
        batch=batch,
    )

    restart_button = shapes.Rectangle(
        WINDOW_WIDTH // 2 - 50,
        third_height,
        100,
        50,
        color=(211, 122, 105),
        batch=batch,
    )
    restart_text = text.Label(
        "Restart",
        font_size=20,
        x=WINDOW_WIDTH // 2,
        y=third_height + 25,
        anchor_x="center",
        anchor_y="center",
        batch=batch,
    )

    score_text = text.Label(
        "",
        font_size=20,
        x=WINDOW_WIDTH // 2,
        y=third_height + 100,
        anchor_x="center",
        anchor_y="center",
        batch=batch,
    )

    image = load_image("pictures/snake_ui.png")
    image_sprite = pyglet.sprite.Sprite(
        image, x=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2 + 100
    )

    return (
        play_button,
        play_text,
        restart_button,
        restart_text,
        score_text,
        image_sprite,
    )
