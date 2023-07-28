from PIL import Image, ImageColor
import numpy as np
import sys

# Configs
# Low value equals more white/black and less color
gray_scale = 90
# white offset - Higher value equals more white, lower means more black
white_offset = 0

black = (0, 0, 0)
white = (255, 255, 255)

try:
    input_img = sys.argv[1]
    output_img = sys.argv[2]
except:
    input_img = "input.png"
    output_img = "output.png"

print(input_img)
img = Image.open(input_img).convert("RGBA")

# More will be added, will need an update then
color_pallet1 = ["#FF4500", "#FFA800", "#FFD635", "#00A368", "#3690EA", "#B44AC0", "#000000", "#FFFFFF"]


def convert_hex_to_rgb():
    return [ImageColor.getrgb(color) for color in color_pallet1]


def find_closest_color(pixel):
    pixel_rgb = pixel[:3]  # Extract only the RGB components, ignore the alpha channel
    min_distance = 250
    closest_color = None
    for color in color_pallet1:
        color_rgb = np.array(color)
        distance = np.linalg.norm(np.array(pixel_rgb) - color_rgb)
        if distance < min_distance:
            min_distance = distance
            closest_color = color

    black_distance = np.linalg.norm(np.array(pixel_rgb) - np.array(black))
    white_distance = np.linalg.norm(np.array(pixel_rgb) - np.array(white)) + white_offset

    if min_distance > gray_scale:
        closest_color = black if black_distance <= white_distance else white
    return closest_color


def replace_pixel_closest_color():
    width, height = img.size
    img_pixels = img.load()

    for x in range(width):
        for y in range(height):
            pixel = img_pixels[x, y]
            closest_color = find_closest_color(pixel)
            img_pixels[x, y] = closest_color

    img.save(output_img)


color_pallet1 = convert_hex_to_rgb()
replace_pixel_closest_color()
