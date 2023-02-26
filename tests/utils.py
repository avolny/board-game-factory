import os
from abc import abstractmethod
from unittest import TestCase
from warnings import warn

import PIL
import numpy as np

from PIL import Image


SHOW_MISMATCH = True
ASSERT_ON = True

if not ASSERT_ON:
    warn('ASSERT_ON = False, tests won\'t fail when dissatisfied')

def get_reference_img_path(folder, *args):
    return get_reference_dir_path(folder) + '_'.join(map(str, args)) + '.png'


def get_reference_dir_path(folder):
    return 'assets/tests/reference/' + folder + '/'


def assert_images_equal(im1: Image, im2: Image, ref_path, args):
    assert im1.mode == im2.mode, im1.mode + " " + im2.mode
    assert im1.size == im2.size, f'{im1.size} {im2.size}'

    for pix1, pix2 in zip(im1.getdata(), im2.getdata()):
        
        if pix1 != pix2:
            print(f'test failed with args: {args}')
            
            if SHOW_MISMATCH:
                diff = Image.fromarray(np.abs(np.asarray(im1) - np.asarray(im2))[:, :, :3].mean(axis=2).astype(np.uint8), mode='L')
                diff.show(title='difference ' + ref_path)

                im1.show(title="reference " + ref_path)
                im2.show(title="tested " + ref_path)
        
            if ASSERT_ON:
                assert pix1 == pix2, str(pix1) + " " + str(pix2) + " " + ref_path
                
            return

    print(f'test passed with args: {args}')
        
        
class ComponentRegressionTestCase(TestCase):
    
    
    @staticmethod
    def generate_test_variants():
        pass

    @staticmethod
    def generate_component(*args):
        pass
    
    @classmethod
    def generate_reference(cls):
        os.makedirs(get_reference_dir_path(cls.__name__), exist_ok=True)
        
        print('Generating:   ' + get_reference_dir_path(cls.__name__))
        
        variants = cls.generate_test_variants()

        for args in variants:
            component = cls.generate_component(*args)

            im = component.image()
            im.save(get_reference_img_path(cls.__name__, *args))
    
    def execute(self):

        for args in self.generate_test_variants():
            im = self.generate_component(*args).image()
            
            path = get_reference_img_path(type(self).__name__, *args)
            im_ref = Image.open(path)

            assert_images_equal(im_ref, im, path, args)