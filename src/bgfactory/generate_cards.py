
from PIL import Image, ImageDraw
from src.bgfactory.pil_patch import *

from src.bgfactory.components.shapes import *

path = 'output/'

card = Rectangle(0, 0, 500, 800, stroke_width=5, stroke_color=(150, 0, 0, 255), fill_color=(150, 150, 150, 255))

box1 = Rectangle(200, 200, 200, 200, stroke_width=3, stroke_color=(255, 0, 0, 255), fill_color=(0, 0, 255, 255))

box1.add(RoundedRectangle(20, 20, 100, 100, 10, stroke_width=5, stroke_color=COLOR_BLACK, fill_color=(0, 255, 0, 128)))

card.add(box1)

im = card.image()

im.show()
im.save(path + 'test.png')