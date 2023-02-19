from bgfactory.components.component import Container
from bgfactory.components.constants import HALIGN_LEFT, HALIGN_CENTER, HALIGN_RIGHT, VALIGN_TOP, VALIGN_MIDDLE, \
    VALIGN_BOTTOM, FILL
from bgfactory.components.layout.vertical_flow_layout import VerticalFlowLayout
from bgfactory.components.shape import Rectangle
from tests.utils import ComponentRegressionTestCase


class TestVerticalFlowLayout2(ComponentRegressionTestCase):
    
    @staticmethod
    def generate_component(box1w, box1h, box2w, box2h):

        rect = Container(0, 0, 600, 600)

        haligns = [HALIGN_LEFT, HALIGN_CENTER, HALIGN_RIGHT]
        valigns = [VALIGN_TOP, VALIGN_MIDDLE, VALIGN_BOTTOM]

        for i, halign in enumerate(haligns):
            for j, valign in enumerate(valigns):
                card = Rectangle(
                    i * 200, j * 200, 200, 200, stroke_width=5, stroke_src=(1, 0, 0, 1),
                    fill_src=(0, 1, 0, 1), padding=(10, 10, 10, 10), layout=VerticalFlowLayout(halign, valign))

                box1 = Rectangle(
                    0, 0, box1w, box1h, stroke_width=2, stroke_src=(0, 0, 0, 1), fill_src=(1, 0, 0, 0.5),
                    margin=(5, 5, 5, 5)
                )

                box2 = Rectangle(
                    0, 0, box2w, box2h, stroke_width=2, stroke_src=(0, 0, 0, 1), fill_src=(1, 0, 0, 0.5),
                    margin=(5, 5, 5, 5)
                )

                card.add(box1)
                card.add(box2)
                rect.add(card)

        return rect
    
    
    @staticmethod
    def generate_test_variants():
        
        args = [
            [20, 20, 30, 30],
            [FILL, 30, 30, FILL],
            ['20%', '20%', FILL, FILL],
            [FILL, '30%', 50, '40%'],
            ['50%', '50%', '50%', '50%'],
            ['20%', '30%', '30%', '40%'],
        ]
        
        return args
    
    def test(self):
        super(TestVerticalFlowLayout2, self).execute()
    