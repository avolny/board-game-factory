from unittest import TestCase

from PIL import Image

from bgfactory.components.constants import HALIGN_LEFT, INFER, HALIGN_CENTER, HALIGN_RIGHT
from bgfactory.components.layout_manager import VerticalFlowLayout
from bgfactory.components.shapes import Rectangle
from tests.utils import get_reference_img_path, assert_images_equal


class VerticalFlowLayoutTest(TestCase):
    
    
    @staticmethod
    def generate_component(halign, boxw, boxh):
        
        card = Rectangle(
            0, 0, 200, 200, stroke_width=5, stroke_color=(255, 0, 0, 255),
            fill_color=(0, 255, 0, 255), padding=(20, 30, 40, 50), layout=VerticalFlowLayout(halign))
        
        box = Rectangle(
            0, 0, boxw, boxh, stroke_width=2, stroke_color=(0, 0, 0, 255), fill_color=(255, 0, 0, 128), 
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
    
    
    def testVerticalFlowLayout(self):
        
        for args in self.generate_test_variants():
            im = self.generate_component(*args).image()
            
            im_ref = Image.open(get_reference_img_path(*args))
            
            assert_images_equal(im_ref, im)
        
        pass
    
    
def generate_reference():
    variants = VerticalFlowLayoutTest.generate_test_variants()

    for args in variants:
        component = VerticalFlowLayoutTest.generate_component(*args)

        im = component.image()
        im.save(get_reference_img_path(*args))
    
    
if __name__ == '__main__':
    
    # generate_reference()
    pass