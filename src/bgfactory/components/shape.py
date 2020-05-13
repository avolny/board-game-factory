from math import pi
from warnings import warn

import cairocffi as cairo

from bgfactory.components.cairo_helpers import adjust_rect_size_by_line_width
from bgfactory.components.component import Container
from bgfactory.components.constants import COLOR_BLACK, COLOR_WHITE
from bgfactory.components.source import convert_source


class Shape(Container):
    
    def __init__(self, x, y, w, h, stroke_width=3, stroke_src=COLOR_BLACK,
                 fill_src=COLOR_WHITE, layout=None, margin=(0, 0, 0, 0), padding=(0, 0, 0, 0)):
        self.stroke_width = stroke_width
        self.stroke_src = convert_source(stroke_src)
        self.fill_src = convert_source(fill_src)
        
        # if self.stroke_src[3] < 1:
        #     warn('The stroke overlaps the fill area, with transparent stroke, you will see the fill through '
        #          'half of the border. If you absolutely need transparent border, create a custom component '
        #          'that renders them with different paths and check yourself for the desired result.')
        
        super(Shape, self).__init__(x, y, w, h, margin, [e + stroke_width for e in padding], layout)
    

class Rectangle(Shape):
    
    def _draw(self, surface: cairo.Surface, w, h):
        
        cr = cairo.Context(surface)
        
        x, y, w, h = adjust_rect_size_by_line_width(0, 0, w, h, self.stroke_width)
        cr.rectangle(x, y, w, h)
        
        cr.set_line_width(self.stroke_width)
        self.fill_src.set(cr, 0, 0, w, h)
        cr.fill_preserve()
        self.stroke_src.set(cr, 0, 0, w, h)
        cr.stroke()


class RoundedRectangle(Shape):

    def __init__(
            self, x, y, w, h, radius=10, stroke_width=3, stroke_src=COLOR_BLACK, 
            fill_src=COLOR_WHITE, layout=None, margin=(0, 0, 0, 0), padding=(0, 0, 0, 0)):
        self.radius = radius

        super(RoundedRectangle, self).__init__(x, y, w, h, stroke_width, stroke_src, fill_src, layout, margin, padding)

    def _draw(self, surface: cairo.Surface, w, h):
        
        cr = cairo.Context(surface)
        x, y, w, h = adjust_rect_size_by_line_width(0, 0, w, h, self.stroke_width)
        x1, y1, x2, y2 = x, y, x + w, y + h

        cr.arc(x1 + self.radius, y1 + self.radius, self.radius, 2 * (pi / 2), 3 * (pi / 2))
        cr.arc(x2 - self.radius, y1 + self.radius, self.radius, 3 * (pi / 2), 4 * (pi / 2))
        cr.arc(x2 - self.radius, y2 - self.radius, self.radius, 0 * (pi / 2), 1 * (pi / 2))  # ;o)
        cr.arc(x1 + self.radius, y2 - self.radius, self.radius, 1 * (pi / 2), 2 * (pi / 2))
        cr.close_path()
        
        cr.set_line_width(self.stroke_width)
        self.fill_src.set(cr, 0, 0, w, h)
        cr.fill_preserve()
        self.stroke_src.set(cr, 0, 0, w, h)
        cr.stroke()
