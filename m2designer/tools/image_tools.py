from PIL import Image, ImageTk, ImageOps
from customtkinter import CTkImage

def open_image(image_path):
    img = Image.open(image_path)
    width, height = img.size
    return make_final_image(img), width, height

def get_image_size(image_path):
    img = Image.open(image_path)
    width, height = img.size
    return width, height

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

    # Corners
    result_image.paste(top_left_corner, (0, 0), top_left_corner)
    result_image.paste(bottom_left_corner, (0, height - bottom_left_corner.height), bottom_left_corner)
    result_image.paste(top_right_corner, (width - top_right_corner.width, 0), top_right_corner)
    result_image.paste(bottom_right_corner, (width - bottom_right_corner.width, height - bottom_right_corner.height), bottom_right_corner)

    return result_image

def stretch_image(image_path, width, height, corner_size):
    if image_path is not None:
        image = Image.open(image_path)

        # Calculate the dimensions of the inner part
        inner_width = width - 2 * corner_size
        inner_height = height - 2 * corner_size

        # Ensure the inner dimensions are valid
        if inner_width <= 0 or inner_height <= 0:
            raise ValueError("Width and height must be greater than twice the corner size.")

        # Crop the corners with fixed size
        top_left_corner = image.crop((0, 0, corner_size, corner_size))
        top_right_corner = image.crop((image.width - corner_size, 0, image.width, corner_size))
        bottom_left_corner = image.crop((0, image.height - corner_size, corner_size, image.height))
        bottom_right_corner = image.crop((image.width - corner_size, image.height - corner_size, image.width, image.height))

        # Crop the inner part of the image
        inner_image = image.crop((
            corner_size,
            corner_size,
            image.width - corner_size,
            image.height - corner_size
        ))

        # Resize the inner part
        resized_inner_image = inner_image.resize((inner_width, inner_height))

        # Create a new blank image with the new size
        new_image = Image.new("RGBA", (width, height))

        # Paste the resized inner part into the new image
        new_image.paste(resized_inner_image, (corner_size, corner_size))

        # Resize and paste the borders
        # Top border
        top_border = image.crop((corner_size, 0, image.width - corner_size, corner_size))
        new_image.paste(top_border.resize((inner_width, corner_size)), (corner_size, 0))

        # Bottom border
        bottom_border = image.crop((corner_size, image.height - corner_size, image.width - corner_size, image.height))
        new_image.paste(bottom_border.resize((inner_width, corner_size)), (corner_size, height - corner_size))

        # Left border
        left_border = image.crop((0, corner_size, corner_size, image.height - corner_size))
        new_image.paste(left_border.resize((corner_size, inner_height)), (0, corner_size))

        # Right border
        right_border = image.crop((image.width - corner_size, corner_size, image.width, image.height - corner_size))
        new_image.paste(right_border.resize((corner_size, inner_height)), (width - corner_size, corner_size))

        # Paste the corners
        # Corners should have the same height and width, otherways those parts may appear blurry
        new_image.paste(top_left_corner, (0, 0))
        new_image.paste(top_right_corner, (width - corner_size, 0))
        new_image.paste(bottom_left_corner, (0, height - corner_size))
        new_image.paste(bottom_right_corner, (width - corner_size, height - corner_size))

        return ImageTk.PhotoImage(new_image)
    else:
        return create_empty_image(width, height)

def create_empty_image(width, height):
    white_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    return make_final_image(white_image)

def create_white_image(width, height):
    empty_image = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    return make_final_image(empty_image)

def make_final_image(image):
    return ImageTk.PhotoImage(image)
