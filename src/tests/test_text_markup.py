from unittest import TestCase

import cairocffi
import pangocffi
from PIL import Image

from bgfactory.components.constants import HALIGN_LEFT, INFER, HALIGN_CENTER, HALIGN_RIGHT, VALIGN_TOP, VALIGN_MIDDLE, \
    VALIGN_BOTTOM
from bgfactory.components.layout_manager import VerticalFlowLayout
from bgfactory.components.shapes import Rectangle
from bgfactory.components.text import TextUniform, FontDescription, TextMarkup
from tests.utils import get_reference_img_path, assert_images_equal, ComponentRegressionTestCase


class TestTextMarkup(ComponentRegressionTestCase):
    TEXT = [
        '<span font_family="Serif" size="30000" foreground="#ffbb00">testing</span>\n<span font_family="Cambria" '
        'background="#ddffcc" size="40000">text</span>',
        '<span font_family="Serif" size="20000" foreground="#ffbb00">testing&amp;</span>\n<span font_family="Cambria" '
        'background="#ddffcc" size="30000">&amp;texting</span>',
    ]
    
    REPLACEMENT = [
        {},
        {'e': Rectangle(0, 0, 15, 25, fill_color=(1, 0, 0, 0.5)),
         'i': Rectangle(0, 0, 13, 25, fill_color=(0, 1, 0, 0.5)),
         '&': Rectangle(0, 0, 11, 25, fill_color=(0, 0, 1, 0.5))}
    ]

    @staticmethod
    def generate_component(halign, valign, textw, texth, textid):
        card = Rectangle(
            0, 0, 200, 200, stroke_width=5, stroke_color=(1, 0, 0, 1),
            fill_color=(0, 1, 0, 0.5), layout=VerticalFlowLayout(halign))
        
        text = TextMarkup(
            0, 0, textw, texth, TestTextMarkup.TEXT[textid], halign=halign, valign=valign, 
            text_replace_map=TestTextMarkup.REPLACEMENT[textid])

        card.add(text)

        return card

    @staticmethod
    def generate_test_variants():
        args = [
            [HALIGN_LEFT, VALIGN_TOP, '100%', '100%', 0],
            [HALIGN_CENTER, VALIGN_TOP, '100%', '100%', 0],
            [HALIGN_RIGHT, VALIGN_TOP, '100%', '100%', 0],
            [HALIGN_LEFT, VALIGN_MIDDLE, '100%', '100%', 0],
            [HALIGN_CENTER, VALIGN_MIDDLE, '100%', '100%', 0],
            [HALIGN_RIGHT, VALIGN_MIDDLE, '100%', '100%', 0],
            [HALIGN_LEFT, VALIGN_BOTTOM, '100%', '100%', 0],
            [HALIGN_CENTER, VALIGN_BOTTOM, '100%', '100%', 0],
            [HALIGN_RIGHT, VALIGN_BOTTOM, '100%', '100%', 0],
            [HALIGN_LEFT, VALIGN_TOP, '100%', '100%', 1],
            [HALIGN_CENTER, VALIGN_TOP, '100%', '100%', 1],
            [HALIGN_RIGHT, VALIGN_TOP, '100%', '100%', 1],
            [HALIGN_LEFT, VALIGN_MIDDLE, '100%', '100%', 1],
            [HALIGN_CENTER, VALIGN_MIDDLE, '100%', '100%', 1],
            [HALIGN_RIGHT, VALIGN_MIDDLE, '100%', '100%', 1],
            [HALIGN_LEFT, VALIGN_BOTTOM, '100%', '100%', 1],
            [HALIGN_CENTER, VALIGN_BOTTOM, '100%', '100%', 1],
            [HALIGN_RIGHT, VALIGN_BOTTOM, '100%', '100%', 1],
        ]

        return args

    def test(self):
        super(TestTextMarkup, self).execute()