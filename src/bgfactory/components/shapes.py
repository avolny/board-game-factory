from PIL import Image
from PIL.ImageDraw import floodfill, ImageDraw

import bgfactory.pil_patch.rounded_rectangle

from bgfactory.components.component import Component, Container
from bgfactory.components.constants import COLOR_BLACK, COLOR_WHITE
from bgfactory.components.layout_manager import AbsoluteLayout
from bgfactory.pil_patch.rounded_rectangle import draw_rounded_rectangle
from bgfactory.profiler import profile


class Shape(Container):
    
    def __init__(self, x, y, w, h, stroke_width=3, stroke_color=COLOR_BLACK, 
                 fill_color=COLOR_WHITE, layout=None, margin=(0,0,0,0), padding=(0,0,0,0)):
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        
        super(Shape, self).__init__(x, y, w, h, margin, [e + stroke_width for e in padding], layout)
    
    def scale(self, val):
        self.stroke_width = int(self.stroke_width * val)
        super(Shape, self).scale(val)
        

class Rectangle(Shape):
    
    def _draw(self, im: Image):
        profile('ImageDraw')
        draw = ImageDraw(im)
        w, h = im.size

        profile('draw.rectangle')
        draw.rectangle(((0, 0), (w - 1, h - 1)), 
                       outline=self.stroke_color, width=self.stroke_width, fill=self.fill_color)
        profile()
        
        super(Rectangle, self)._draw(im)


class RoundedRectangle(Shape):
    
    def __init__(
            self, x, y, w, h, radius=10, stroke_width=3, stroke_color=COLOR_BLACK, 
            fill_color=COLOR_WHITE, layout=None, margin=(0,0,0,0), padding=(0,0,0,0)):
        self.radius = radius
        
        super(RoundedRectangle, self).__init__(x, y, w, h, stroke_width, stroke_color, fill_color, layout, margin, padding)
        
    def scale(self, val):
        self.radius = int(self.radius * val)
        super(Shape, self).scale(val)
    
    def _draw(self, im: Image):
        profile('ImageDraw')
        # draw = ImageDraw(im)
        w, h = im.size
        
        profile('draw.rounded_rectangle')
        im_ = draw_rounded_rectangle(w, h, ((0, 0), (w, h)), self.radius, self.stroke_color, self.fill_color, self.stroke_width)

        profile('paste.rounder_rectangle')
        im.paste(im_, (0, 0), im_)
        
        # draw.rounded_rectangle(((0, 0), (w - 1, h - 1)),
        #                corner_radius=self.radius, outline=self.stroke_color, width=self.stroke_width)
        # profile('draw.floodfill')
        # floodfill(im, (int((w - 1) / 2), int((h - 1) / 2)), self.fill_color)
        profile()

        super(RoundedRectangle, self)._draw(im)


class Ellipse(Shape):
    def _draw(self, im: Image):
        draw = ImageDraw(im)
        w, h = im.size

        draw.rectangle(((0, 0), (w - 1, h - 1)),
                       outline=self.stroke_color, width=self.stroke_width, fill=self.fill_color)

        super(Ellipse, self)._draw(im)