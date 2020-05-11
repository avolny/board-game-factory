from bgfactory.components.component import Container
from bgfactory.components.constants import HALIGN_LEFT, HALIGN_CENTER, HALIGN_RIGHT, VALIGN_TOP, VALIGN_MIDDLE, \
    VALIGN_BOTTOM, FILL
from bgfactory.components.layout.horizontal_flow_layout import HorizontalFlowLayout
from bgfactory.components.shapes import Rectangle
from tests.utils import ComponentRegressionTestCase


class TestHorizontalFlowLayout2(ComponentRegressionTestCase):

    @staticmethod
    def generate_component(box1w, box1h, box2w, box2h):

        rect = Container(0, 0, 600, 600)

        haligns = [HALIGN_LEFT, HALIGN_CENTER, HALIGN_RIGHT]
        valigns = [VALIGN_TOP, VALIGN_MIDDLE, VALIGN_BOTTOM]

        for i, halign in enumerate(haligns):
            for j, valign in enumerate(valigns):
                card = Rectangle(
                    i * 200, j * 200, 200, 200, stroke_width=5, stroke_color=(1, 0, 0, 1),
                    fill_color=(0, 1, 0, 1), padding=(10, 10, 10, 10), layout=HorizontalFlowLayout(halign, valign))

                box1 = Rectangle(
                    0, 0, box1w, box1h, stroke_width=2, stroke_color=(0, 0, 0, 1), fill_color=(1, 0, 0, 0.5),
                    margin=(5, 5, 5, 5)
                )

                box2 = Rectangle(
                    0, 0, box2w, box2h, stroke_width=2, stroke_color=(0, 0, 0, 1), fill_color=(1, 0, 0, 0.5),
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
            [30, FILL, FILL, 30],
            ['20%', '20%', FILL, FILL],
            ['30%', FILL, 50, '40%'],
            ['50%', '50%', '50%', '50%'],
            ['20%', '30%', '30%', '40%'],
        ]

        return args

    def test(self):
        super(TestHorizontalFlowLayout2, self).execute()
