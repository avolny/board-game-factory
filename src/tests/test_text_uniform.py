import cairocffi
import pangocffi

from bgfactory.components.constants import HALIGN_LEFT, INFER, HALIGN_CENTER, HALIGN_RIGHT, VALIGN_TOP, VALIGN_MIDDLE, \
    VALIGN_BOTTOM
from bgfactory.components.layout.vertical_flow_layout import VerticalFlowLayout
from bgfactory.components.shapes import Rectangle
from bgfactory.components.text import TextUniform, FontDescription
from tests.utils import ComponentRegressionTestCase


class TestTextUniform(ComponentRegressionTestCase):
    TEXT = ['testing\ntext']

    @staticmethod
    def generate_component(halign, valign, textw, texth, textid):
        card = Rectangle(
            0, 0, 200, 200, stroke_width=5, stroke_color=(1, 0, 0, 1),
            fill_color=(0, 1, 0, 0.9), layout=VerticalFlowLayout(halign))
        
        font_desc = FontDescription(
            "Arial", 24, pangocffi.Weight.BOLD, pangocffi.Style.OBLIQUE)
        
        text = TextUniform(
            0, 0, textw, texth, TestTextUniform.TEXT[textid], font_desc, halign=halign, valign=valign,
            stroke_width=3, color=(0.3, 0.7, 0.3, 0.5), stroke_color=(0.7, 0.3, 0.7, 0.9), 
            outline_line_join=cairocffi.LINE_JOIN_ROUND
        )

        card.add(text)

        return card

    @staticmethod
    def generate_test_variants():
        args = [
            [HALIGN_LEFT, VALIGN_TOP, '100%', '100%', 0],
            [HALIGN_LEFT, VALIGN_TOP, 150, '100%', 0],
            [HALIGN_LEFT, VALIGN_TOP, INFER, '100%', 0],
            [HALIGN_LEFT, VALIGN_TOP, INFER, INFER, 0],
            [HALIGN_CENTER, VALIGN_TOP, '100%', '100%', 0],
            [HALIGN_RIGHT, VALIGN_TOP, '100%', '100%', 0],
            [HALIGN_LEFT, VALIGN_MIDDLE, '100%', '100%', 0],
            [HALIGN_CENTER, VALIGN_MIDDLE, '100%', '100%', 0],
            [HALIGN_RIGHT, VALIGN_MIDDLE, '100%', '100%', 0],
            [HALIGN_LEFT, VALIGN_BOTTOM, '100%', '100%', 0],
            [HALIGN_CENTER, VALIGN_BOTTOM, '100%', '100%', 0],
            [HALIGN_RIGHT, VALIGN_BOTTOM, '100%', '100%', 0],
        ]

        return args

    def test(self):
        super(TestTextUniform, self).execute()