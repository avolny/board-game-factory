from bgfactory.components.constants import HALIGN_LEFT, INFER, HALIGN_CENTER, HALIGN_RIGHT
from bgfactory.components.layout.vertical_flow_layout import VerticalFlowLayout
from bgfactory.components.shape import Rectangle
from tests.utils import ComponentRegressionTestCase


class TestVerticalFlowLayout(ComponentRegressionTestCase):
    
    @staticmethod
    def generate_component(halign, boxw, boxh):
        
        card = Rectangle(
            0, 0, 200, 200, stroke_width=5, stroke_src=(1, 0, 0, 1),
            fill_src=(0, 1, 0, 1), padding=(20, 30, 40, 50), layout=VerticalFlowLayout(halign))
        
        box = Rectangle(
            0, 0, boxw, boxh, stroke_width=2, stroke_src=(0, 0, 0, 1), fill_src=(1, 0, 0, 0.5),  
            margin=(5, 10, 15, 20)
        )
        
        card.add(box)

        return card
    
    
    @staticmethod
    def generate_test_variants():
        
        args = [
            [HALIGN_LEFT, '100%', '100%'],
            [HALIGN_LEFT, 20, '100%'],
            [HALIGN_LEFT, INFER, '100%'],
            [HALIGN_LEFT, 20, 20],
            [HALIGN_RIGHT, 20, 20],
            [HALIGN_CENTER, 20, 20],
        ]
        
        return args
    
    def test(self):
        super(TestVerticalFlowLayout, self).execute()
    