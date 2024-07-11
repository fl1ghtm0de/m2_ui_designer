from PIL import Image, ImageTk

def create_tilted_image(image_path, width, height):
    small_image = Image.open(image_path)
    small_width, small_height = small_image.size

    tiled_image = Image.new('RGB', (width, height))

    for i in range(0, width, small_width):
        for j in range(0, height, small_height):
            tiled_image.paste(small_image, (i, j))

    return tiled_image

def add_borders(tiled_image, border_images, button_offset=0):
    width, height = tiled_image.size
    result_image = Image.new('RGB', (width, height))

    # Paste the tiled image in the center
    result_image.paste(tiled_image, (0, 0))

    top_border = Image.open(border_images["top"])
    left_border = Image.open(border_images["left"])
    bottom_border = Image.open(border_images["bottom"])
    right_border = Image.open(border_images["right"])

    top_left_corner = Image.open(border_images["top_left_corner"])
    bottom_left_corner = Image.open(border_images["bottom_left_corner"])
    bottom_right_corner = Image.open(border_images["bottom_right_corner"])
    top_right_corner = Image.open(border_images["top_right_corner"])

    top_width, top_height = top_border.size
    left_width, left_height = left_border.size
    bottom_width, bottom_height = bottom_border.size
    right_width, right_height = right_border.size

    close_button = Image.open(border_images["close_button"])
    minimize_button = Image.open(border_images["minimize_button"])

    # Top border
    for i in range(top_left_corner.width, width - top_right_corner.width, top_width):
        result_image.paste(top_border, (i, 0))
    # Bottom border
    for i in range(bottom_left_corner.width, width - bottom_right_corner.width, bottom_width):
        result_image.paste(bottom_border, (i, height - bottom_height))
    # Left border
    for i in range(top_left_corner.height, height - bottom_left_corner.height, left_height):
        result_image.paste(left_border, (0, i))
    # Right border
    for i in range(top_right_corner.height, height - bottom_right_corner.height, right_height):
        result_image.paste(right_border, (width - right_width, i))

    top_right_corner.paste(close_button, (top_right_corner.width - close_button.width, button_offset), close_button)
    top_right_corner.paste(minimize_button, (top_right_corner.width - close_button.width - minimize_button.width, button_offset), minimize_button)

    # Corners
    result_image.paste(top_left_corner, (0, 0))
    result_image.paste(bottom_left_corner, (0, height - bottom_left_corner.height))
    result_image.paste(top_right_corner, (width - top_right_corner.width, 0))
    result_image.paste(bottom_right_corner, (width - bottom_right_corner.width, height - bottom_right_corner.height))

    return result_image

def make_final_image(tilted_image):
    return ImageTk.PhotoImage(tilted_image)