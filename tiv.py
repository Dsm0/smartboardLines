#!/usr/bin/env python3
from __future__ import print_function  # accomodate Python 2

from PIL import Image, GifImagePlugin
from cairosvg import svg2png
import click
import io
import numpy
import sys
import tiv
import os
from colors import *
# for i in range(256):
#     print(color('Color #%d' % i, fg=i))


rows, columns = os.popen('stty size', 'r').read().split()
rows = int(rows)
columns = int(columns)

def ansi(r, g, b, a=0):
    rgbval = "rgb(" + str(r) + ","+ str(g) + ","+ str(b) + ")"
    return(color('█', rgbval))
    #print("r: " + str(r) + "  g: " + str(g) +" b: " + str(b))
    # def get_code():
    #     if r == g == b:
    #         if r < 8:
    #             return 16
    #         if r > 248:
    #             return 231
    #         return round(((r - 8) / 247) * 24) + 232
    #     return 16 \
    #         + (36 * round(r / 255 * 5)) \
    #         + (6 * round(g / 255 * 5)) \
    #         + round(b / 255 * 5)
    # return "\x1b[48;5;{}m \x1b[0m".format(int(get_code()))



def print_image(image, width=69, aspect_ratio=0.5):
    # print("inPrint")
    try:
        # print("inTry")
        img = Image.open(image)
        # print(img)
    except:
        png_data = svg2png(url=image)
        img = Image.open(io.BytesIO(png_data))

    if hasattr(img, 'is_animated') and img.is_animated:
        img = img.convert('RGBA')
        print(img)
    w = width
    h = int((img.height / img.width) * w * aspect_ratio)
    img = img.resize((w,h), Image.ANTIALIAS)
    img_arr = numpy.asarray(img)
    h,w,_ = img_arr.shape
    image_string = ''
    for x in range(h):
        # print("before Print")
        image_string += ''.join([ansi(*p) for p in img_arr[x]]) + '\n'
        # print(image_string)
    return(image_string)


@click.command()
# @click.version_option(version=tiv.__version__,
#     message="%(prog)s %(version)s - {}".format(tiv.__copyright__))
@click.argument('images', nargs=-1, required=True, type=str)
@click.option('-w', '--width', default=(columns-20), show_default=True)
@click.option('-a', '--aspect-ratio', default=0.5, show_default=True)
def cli(images, width, aspect_ratio):
    errors = 0
    for image in images:
        try:
            print("inTry")
            print_image(
                image=image,
                width=width,
                aspect_ratio=aspect_ratio,
                )
        except FileNotFoundError:
            print('Image not found: ' + image)
            errors += 1
        except Exception as e:
            print(str(e) + ': ' + image)
            errors += 1
    return errors

if __name__ == '__main__':
    cli()
