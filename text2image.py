# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

img = Image.new('L', (128, 128), 255)
draw = ImageDraw.Draw(img)
text_to_draw = unicode('xxs', 'utf-8')
font = ImageFont.truetype('fonts/NotoSansCJKsc-Regular.otf', 12)
draw.text((2, 2), text_to_draw, font=font)
del draw

img.save('build/image.png')