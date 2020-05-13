from bgfactory.components.constants import HALIGN_LEFT, INFER, HALIGN_CENTER, HALIGN_RIGHT, VALIGN_TOP, VALIGN_MIDDLE, \
    VALIGN_BOTTOM
from bgfactory.components.layout.vertical_flow_layout import VerticalFlowLayout
from bgfactory.components.shape import Rectangle
from bgfactory.components.text import TextUniform
from tests.utils import ComponentRegressionTestCase


class TestTextAlignment(ComponentRegressionTestCase):
    
    TEXT = ['testing\ntext']
    
    @staticmethod
    def generate_component(halign, valign, textw, texth, textid):
        card = Rectangle(
            0, 0, 200, 200, stroke_width=5, stroke_src=(1, 0, 0, 1),
            fill_src=(0, 1, 0, 0.9), layout=VerticalFlowLayout(halign))
        
        text = TextUniform(
            0, 0, textw, texth, TestTextAlignment.TEXT[textid], halign=halign, valign=valign)

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
        super(TestTextAlignment, self).execute()