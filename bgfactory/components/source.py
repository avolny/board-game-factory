from abc import ABC, abstractmethod
from collections.abc import Iterable

import cairocffi as cairo
from cairocffi import Context

from bgfactory.components.constants import INFER, FILL, VALIGN_TOP, VALIGN_MIDDLE, VALIGN_BOTTOM, HALIGN_LEFT, \
    HALIGN_CENTER, HALIGN_RIGHT
from bgfactory.components.utils import is_percent, parse_percent


def convert_source(src):
    if isinstance(src, Iterable):
        src = tuple(src)
        
        if len(src) == 3:
            return RGBSource(*src)
        elif len(src) == 4:
            return RGBASource(*src)
        else:
            raise ValueError('When using a tuple as a fill/stroke source, it must have '
                             'either length 3 (RGB) or 4 (RGBA)')
    elif isinstance(src, Source):
        return src
    elif src is None:
        return src
    else:
        raise ValueError('Fill/stroke source not recognized, type:{}, {}'.format(type(src), src))
        

class Source(ABC):
    
    @abstractmethod
    def set(self, cairo_context: Context, x, y, w, h):
        """
        Set this source for given context
        :param cairo_context: context into which set this source 
        :param x: x coordinate of the caller
        :param y: y coordinate of the caller
        :param w: width of the caller
        :param h: height of the caller
        :return: 
        """
        pass


class RGBSource(Source):
    
    def __init__(self, r, g, b):
        self.rgb = (r, g, b)
        
    def set(self, cairo_context: Context, x, y, w, h):
        cairo_context.set_source_rgb(*self.rgb)
        
        
class RGBASource(Source):
    
    def __init__(self, r, g, b, a):
        self.rgba = (r, g, b, a)
        
    def set(self, cairo_context: Context, x, y, w, h):
        cairo_context.set_source_rgba(*self.rgba)


AUTO = 'auto'

    
class PNGSource(Source):
    
    def __init__(self, path, x=0, y=0, w=FILL, h=FILL, halign=HALIGN_LEFT, valign=VALIGN_TOP):
        """
        Use this to render a png image as a background or use it for the strokes - borders/lines/text/etc.
        :param path: path to the png file
        :param x: x coordinate of the png in the coordinate space of the target
        :param y: y coordinate of the png in the coordinate space of the target
        :param w: render size of the image: int/float, 'n%', FILL/INFER or AUTO. int/float will rescale the image width
        to set pixel value, 'n%' and FILL will scale the image according to the target surface size, INFER will use
        the images size. AUTO will compute the width from the height while maintaining the original image's aspect ratio.
        Setting both width and height to AUTO is the same as setting them both to INFER
        :param h: render size of the image: int/float, 'n%', FILL/INFER or AUTO. int/float will rescale the image height
        to set pixel value, 'n%' and FILL will scale the image according to the target surface size, INFER will use
        the images size. AUTO will compute the width from the width while maintaining the original image's aspect ratio.
        Setting both width and height to AUTO is the same as setting them both to INFER
        :param valign: determines how the png image will be vertically aligned w.r.t. the target. For x=0, y=0, w=FILL, h=AUTO,
        the VALIGN_TOP will result in the image being aligned with the top edge, VALIGN_MIDDLE in the middle,
        and VALIGN_BOTTOM with the bottom edge
        :param halign: determines how the png image will be horizontally aligned w.r.t. the target. For x=0, y=0, w=AUTO, h=FILL,
        the HALIGN_LEFT will result in the image being aligned with the left edge, HALIGN_CENTER in the center,
        and HALIGN_RIGHT with the right edge
        """
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.halign = halign
        self.valign = valign
        
        self.path = path

    def set(self, cairo_context: Context, x, y, w, h):
        
        surface_img = cairo.ImageSurface.create_from_png(str(self.path))
        
        iw = surface_img.get_width()
        ih = surface_img.get_height()
        
        if self.w == AUTO and self.h == AUTO:
            self.w = FILL
            self.h = FILL
        
        if self.w == INFER:
            w_target = iw
        elif self.w == FILL:
            w_target = w
        elif is_percent(self.w):
            w_target = w * parse_percent(self.w)
        elif isinstance(self.w, (float, int)):
            w_target = self.w
        elif self.w == AUTO:
            pass
        else:
            raise ValueError('unrecognized width: {}'.format(self.w))
        
        if self.h == INFER:
            h_target = ih
        elif self.h == FILL:
            h_target = h
        elif is_percent(self.h):
            h_target = h * parse_percent(self.h)
        elif isinstance(self.h, (float, int)):
            h_target = self.h
        elif self.h == AUTO:
            pass
        else:
            raise ValueError('unrecognized height: {}'.format(self.h))
        
        if self.w == AUTO:
            w_target = h_target * iw / ih
        if self.h == AUTO:
            h_target = w_target * ih / iw
        
        w_target = int(w_target)
        h_target = int(h_target)
        
        scalex = w_target / iw
        scaley = h_target / ih
        
        # print(iw, ih)
        # print(w_target, h_target)
        # print(scalex, scaley)
        
        output_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w_target, h_target)
        cr = cairo.Context(output_surface)
        cr.scale(scalex, scaley)
        cr.set_source_surface(surface_img)
        cr.paint()
        
        if self.halign == HALIGN_LEFT:
            x_ = self.x + x
        elif self.halign == HALIGN_CENTER:
            x_ = self.x + x + w / 2 - w_target / 2
        elif self.halign == HALIGN_RIGHT:
            x_ = self.x + x + w - w_target
        else:
            raise ValueError('Invalid halign value {}'.format(self.halign))
        
        if self.valign == VALIGN_TOP:
            y_ = self.y + y
        elif self.valign == VALIGN_MIDDLE:
            y_ = self.y + y + h / 2 - h_target / 2
        elif self.valign == VALIGN_BOTTOM:
            y_ = self.y + y + h - h_target
        else:
            raise ValueError('Invalid valign value {}'.format(self.valign))
        
        cairo_context.set_source_surface(output_surface, x_, y_)
