from PIL import Image


def get_reference_img_path(*args):
    return '../../assets/tests/reference/' + '_'.join(map(str, args)) + '.png'


def assert_images_equal(im1: Image, im2: Image):
    assert im1.mode == im2.mode, im1.mode + " " + im2.mode
    assert im1.size == im2.size
    
    for pix1, pix2 in zip(im1.getdata(), im2.getdata()):
        assert pix1 == pix2, pix1 + " " + pix2