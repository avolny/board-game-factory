
from PIL import Image, ImageDraw

from bgfactory.components.constants import COLOR_BLACK, COLOR_TRANSPARENT
from bgfactory.components.text import Text
from bgfactory.components.utils import perc
from bgfactory.pil_patch import *

from bgfactory.components.shapes import *

path = 'output/'

card = Rectangle(0, 0, 500, 800, stroke_width=5, stroke_color=(150, 0, 0, 255), fill_color=(150, 150, 150, 255))

# box1 = Rectangle(200, 200, 200, 200, stroke_width=3, stroke_color=(255, 0, 0, 255), fill_color=(0, 0, 255, 255))

# box1.add(RoundedRectangle(20, 20, 100, 100, 10, stroke_width=5, stroke_color=COLOR_BLACK, fill_color=(0, 255, 0, 128)))

# card.add(box1)


valigns = [Text.VALIGN_TOP, Text.VALIGN_MIDDLE, Text.VALIGN_BOTTOM]
haligns = [Text.HALIGN_LEFT, Text.HALIGN_CENTER, Text.HALIGN_RIGHT]

for i in range(3):
    for j in range(3):
        print(i, j)
        
        x = 5
        y = 5
        w = 30
        h = 30
        text_rect = Rectangle(perc(x + w * i), perc(y + h * j), perc(w), perc(h), stroke_width=1, stroke_color=COLOR_BLACK,
                              fill_color=COLOR_TRANSPARENT)
        # text = Text('3%', '3%', '94%', '94%', "This is\ntext", font_size=20, halign=haligns[i], valign=valigns[j], spacing=-3,
        #             yoffset=-4)
        text = Text('3%', '3%', 'infer', 'infer', "This is\ntext", font_size=20, halign=haligns[i], valign=valigns[j],
                    spacing=-3, yoffset=-4)

        text_rect.add(text)

        card.add(text_rect)

im = card.image()

im.show()
im.save(path + 'test.png')