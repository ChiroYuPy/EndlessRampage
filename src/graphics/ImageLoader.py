import pygame


def load_image(image_path, scale=1, color_key=(255, 255, 255), transparency=True, alpha=255):
    try:
        image = pygame.image.load("src/assets/images/" + image_path)
    except pygame.error as e:
        print(f"Error loading image: {image_path}")
        raise e

    for x in range(image.get_width()):
        for y in range(image.get_height()):
            pixel_color = image.get_at((x, y))
            if pixel_color == (0, 0, 0, 0) and transparency:
                continue

            pixel_value_r = pixel_color.r * color_key[0] / 255
            pixel_value_g = pixel_color.g * color_key[1] / 255
            pixel_value_b = pixel_color.b * color_key[2] / 255

            new_color = pygame.Color(int(pixel_value_r), int(pixel_value_g), int(pixel_value_b), alpha)
            image.set_at((x, y), new_color)

    image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))

    return image
