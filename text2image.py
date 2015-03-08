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


def hex2rgb(hex_color):
    return struct.unpack('BBB', hex_color.decode('hex'))


def generate_image(text, filename, background_color, font_color):
    img = Image.new('RGB', (128, 128), background_color)
    draw = ImageDraw.Draw(img)
    text_to_draw = unicode(text, 'utf-8')
    font = ImageFont.truetype('fonts/NotoSansCJKsc-Regular.otf', 24)
    draw.text((2, 50), text_to_draw, font=font, fill=font_color)
    del draw
    img = add_corners(img, 20)
    img.save('build/' + filename + '.png')


ConfigColor.read("./color.ini")

bg_colors = []
font_colors = []

for color_name, color in ConfigColor.items('Color'):
    bg_colors.append(color.replace('#', '').split(',')[0])
    font_colors.append(color.replace('#', '').split(',')[1])

colors_length = ConfigColor.items('Color').__len__()

for word, filename in ConfigColor.items('Text'):
    random_int = randint(0, colors_length - 1)
    print word, filename.replace('#', '')
    bg_color = hex2rgb(bg_colors[random_int])
    font_color = hex2rgb(font_colors[random_int])
    print bg_colors[random_int], font_colors[random_int]
    generate_image(word.upper(), filename, bg_color, font_color)