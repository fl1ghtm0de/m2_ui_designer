from PIL import Image
from customtkinter import CTkImage

def create_tiled_image(image_path, width, height):
    small_image = Image.open(image_path)
    small_width, small_height = small_image.size

    tiled_image = Image.new('RGB', (width, height))

    for i in range(0, width, small_width):
        for j in range(0, height, small_height):
            tiled_image.paste(small_image, (i, j))

    return tiled_image

def add_borders(tiled_image, border_images):
    width, height = tiled_image.size
    result_image = Image.new('RGBA', (width, height))

    # Paste the tiled image in the center
    result_image.paste(tiled_image.convert('RGBA'), (0, 0))

    top_border = Image.open(border_images["top"]).convert('RGBA')
    left_border = Image.open(border_images["left"]).convert('RGBA')
    bottom_border = Image.open(border_images["bottom"]).convert('RGBA')
    right_border = Image.open(border_images["right"]).convert('RGBA')

    top_left_corner = Image.open(border_images["top_left_corner"]).convert('RGBA')
    bottom_left_corner = Image.open(border_images["bottom_left_corner"]).convert('RGBA')
    bottom_right_corner = Image.open(border_images["bottom_right_corner"]).convert('RGBA')
    top_right_corner = Image.open(border_images["top_right_corner"]).convert('RGBA')

    # close_button = Image.open(border_images["close_button"]).convert('RGBA')
    # minimize_button = Image.open(border_images["minimize_button"]).convert('RGBA')

    top_width, top_height = top_border.size
    left_width, left_height = left_border.size
    bottom_width, bottom_height = bottom_border.size
    right_width, right_height = right_border.size

    # Top border
    for i in range(top_left_corner.width, width - top_right_corner.width, top_width):
        result_image.paste(top_border, (i, 0), top_border)
    # Bottom border
    for i in range(bottom_left_corner.width, width - bottom_right_corner.width, bottom_width):
        result_image.paste(bottom_border, (i, height - bottom_height), bottom_border)
    # Left border
    for i in range(top_left_corner.height, height - bottom_left_corner.height, left_height):
        result_image.paste(left_border, (0, i), left_border)
    # Right border
    for i in range(top_right_corner.height, height - bottom_right_corner.height, right_height):
        result_image.paste(right_border, (width - right_width, i), right_border)

    # Add close and minimize buttons to the top right corner with offsets
    # top_right_corner.paste(close_button, (top_right_corner.width - close_button.width - button_offset, button_offset), close_button)
    # top_right_corner.paste(minimize_button, (top_right_corner.width - close_button.width - minimize_button.width - 2 * button_offset, button_offset), minimize_button)

    # Corners
    result_image.paste(top_left_corner, (0, 0), top_left_corner)
    result_image.paste(bottom_left_corner, (0, height - bottom_left_corner.height), bottom_left_corner)
    result_image.paste(top_right_corner, (width - top_right_corner.width, 0), top_right_corner)
    result_image.paste(bottom_right_corner, (width - bottom_right_corner.width, height - bottom_right_corner.height), bottom_right_corner)

    return result_image

def make_final_image(tilted_image):
    return CTkImage(light_image=tilted_image, size=(tilted_image.width, tilted_image.height))
