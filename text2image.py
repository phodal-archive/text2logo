# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import ConfigParser
import struct
from random import randint

ConfigColor = ConfigParser.ConfigParser()


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    image = ImageDraw.Draw(circle)
    image.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def generate_image(text, key):
    global img, draw, text_to_draw, font
    img = Image.new('RGB', (128, 128), color)
    draw = ImageDraw.Draw(img)
    text_to_draw = unicode(text, 'utf-8')
    font = ImageFont.truetype('fonts/NotoSansCJKsc-Regular.otf', 24)
    draw.text((2, 50), text_to_draw, font=font)
    del draw
    img = add_corners(img, 20)
    img.save('build/' + key + '.png')


ConfigColor.read("./color.ini")

colors = []

# items in section 'NODE': key, value pairs
for color_name, color in ConfigColor.items('Color'):
    colors.append(color.replace('#', ''))

colors_length = ConfigColor.items('Color').__len__()

for word, filename in ConfigColor.items('Text'):
    random_int = randint(1, colors_length)
    print word, filename.replace('#', '')
    rgbstr = colors[random_int]
    color = struct.unpack('BBB', rgbstr.decode('hex'))
    generate_image(word.upper(), filename)