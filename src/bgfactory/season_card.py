from PIL import Image, ImageDraw

from src.bgfactory.components.constants import COLOR_BLACK, COLOR_TRANSPARENT, HALIGN_LEFT, HALIGN_CENTER, HALIGN_RIGHT, \
    VALIGN_BOTTOM, VALIGN_MIDDLE, VALIGN_TOP
from src.bgfactory.components.layout_manager import VerticalFlowLayout
from src.bgfactory.components.text import Text
from src.bgfactory.components.utils import perc
from src.bgfactory.pil_patch import *

from src.bgfactory.components.shapes import *

path = '../../output/'

padding = [20] * 4

card = RoundedRectangle(
    0, 0, 731, 1038, margin=(10, 10, 10, 10), radius=40, stroke_width=5, stroke_color=(0, 0, 0, 255), 
    fill_color=COLOR_WHITE, padding=padding, layout=VerticalFlowLayout(HALIGN_CENTER))

title = Text(
    0, 0, '100%', '8%', 'Seasonal Event', font_size=50, stroke_width=2, 
    stroke_color=COLOR_BLACK, color=COLOR_TRANSPARENT, margin=(5, 0, 0, 0))

card.add(title)

TEXT = ['Spring', 'Summer', 'Autumn', 'Winter']

for i in range(4):

    box = RoundedRectangle(
        0, 0, '100%', '23%', radius=30, stroke_width=3, stroke_color=COLOR_BLACK,
        fill_color=COLOR_TRANSPARENT, padding=(0, 0, 0, 0), margin=(0, 0, 0, 5),
        layout=VerticalFlowLayout(HALIGN_LEFT))
    
    text = Text(0, 0, 'infer', 'infer', TEXT[i], font_size=30, margin=(20, 5, 0, 0))
    
    box.add(text)
    card.add(box)

scale = 0.28

im = card.image()
im = im.resize((int(im.size[0] * scale), int(im.size[1] * scale)))

im.show()
im.save(path + 'test.png')