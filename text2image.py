# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import ConfigParser
import struct

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


ConfigColor.read("./color.ini")
# print ConfigColor.sections()
rgbstr = '1abc9c'
color = struct.unpack('BBB', rgbstr.decode('hex'))

img = Image.new('RGB', (128, 128), color)
draw = ImageDraw.Draw(img)

text_to_draw = unicode('自动化测试', 'utf-8')
font = ImageFont.truetype('fonts/NotoSansCJKsc-Regular.otf', 24)
draw.text((2, 50), text_to_draw, font=font)
del draw
img = add_corners(img, 20)
img.save('build/image.png')