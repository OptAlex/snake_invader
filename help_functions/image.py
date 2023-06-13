import pyglet

def load_image(image_path):
    """
    Helper function to load and center an image.

    Args:
        image_path (str): Path to the image file.

    Returns:
        Image: Pyglet Image object with centered anchor points.
    """
    image = pyglet.image.load(image_path)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

    return image
