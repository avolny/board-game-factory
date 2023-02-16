from bgfactory.components.constants import HALIGN_LEFT, INFER, HALIGN_CENTER, HALIGN_RIGHT, COLOR_RED, COLOR_GREEN
from bgfactory.components.layout.vertical_flow_layout import VerticalFlowLayout
from bgfactory.components.regular_polygon import RegularPolygon
from bgfactory.components.shape import Rectangle
from tests.utils import ComponentRegressionTestCase


class TestRegularPolygon(ComponentRegressionTestCase):
    
    @staticmethod
    def generate_component(num_side, rotation, radius, stroke_width):
        
        poly = RegularPolygon(0, 0, num_side, radius, rotation, stroke_width=stroke_width,
                              stroke_src=COLOR_RED, fill_src=COLOR_GREEN)

        return poly

    @staticmethod
    def generate_test_variants():

        num_sides = [3, 4, 5, 6, 9]
        rotations = [0, 0.25, 0.5, 0.75, 1]

        radii = [50, 100]
        stroke_widths = [2, 5]

        args = []

        for radius, stroke_width in zip(radii, stroke_widths):
            for num_side in num_sides:
                for rotation in rotations:
                    args.append((num_side, rotation, radius, stroke_width))

        return args
    
    def test(self):
        super(TestRegularPolygon, self).execute()
    