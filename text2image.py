# -*- coding: utf-8 -*-
from _ctypes import sizeof
from PIL import Image, ImageDraw, ImageFont
import ConfigParser
import struct

from random import randint
from BeautifulSoup import BeautifulSoup

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


def cal_text_length(text):
    en_text_length = 13
    zh_text_length = 22
    zh_text_size = 3
    offset = 8

    if BeautifulSoup(text).originalEncoding == 'utf-8':
        w = zh_text_length * text.__len__() / zh_text_size + offset
    else:
        w = en_text_length * text.__len__()
    return w


def generate_image(text, file_name, background_color, fill_color):
    width = 128
    height = 128
    font_size = 24
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)
    text_to_draw = unicode(text, 'utf-8')
    font = ImageFont.truetype('fonts/NotoSansCJKsc-Regular.otf', font_size)
    w = cal_text_length(text)
    draw.text(((width - w) / 2, (height - font_size) / 2), text_to_draw, font=font, fill=fill_color)
    del draw
    img = add_corners(img, 20)
    img.save('build/' + file_name + '.png')


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