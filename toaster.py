# toaster.py
#
# makes a new piece of toast

from random import gauss, randint
from PIL import Image, ImageMath


def toast_bread():
    algorithm = "255*(1-(1-a/255)/(b/255))"
    bread_filename = "bread.jpg"
    mask_filename = "mask.png"
    toast_filename = "toast.png"

    bread = Image.open(bread_filename)
    width, height = bread.size

    mask = Image.open(mask_filename)
    pixels = mask.load()

    for x in range(width):
        for y in range(height):
            if pixels[x, y] != 255:
                color = 255 - 30*randint(0, 2)*randint(1, 2)
                pixels[x, y] = color

    mask = mask.convert(mode="F")
    split = [channel.convert(mode="F") for channel in bread.split()]

    channels = [ImageMath.eval(algorithm, a=channel, b=mask).convert("L") for channel in split]

    toast = Image.merge("RGB", channels)
    toast.save(toast_filename)

    return toast_filename

    