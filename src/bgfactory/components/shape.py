import math
from math import pi
from warnings import warn

import cairocffi as cairo

from bgfactory.components.cairo_helpers import adjust_rect_size_by_line_width
from bgfactory.components.component import Container
from bgfactory.components.constants import COLOR_BLACK, COLOR_WHITE
from bgfactory.components.source import convert_source


class Shape(Container):

    def __init__(self, x, y, w, h, stroke_width=3, stroke_src=COLOR_BLACK,
                 fill_src=COLOR_WHITE, layout=None, margin=(0, 0, 0, 0), padding=(0, 0, 0, 0),
                 dash=None, line_cap=None, line_join=None, tolerance=0.1):
        
        if stroke_src[3] < 1:
            warn('The stroke overlaps the fill area, with transparent stroke, you will see the fill through '
                 'half of the border. If you absolutely need transparent border, create a custom component '
                 'that renders them with different paths and check yourself for the desired result.')
        
        self.stroke_width = stroke_width
        self.stroke_src = convert_source(stroke_src)
        self.fill_src = convert_source(fill_src)
        self.dash = dash
        self.line_cap = line_cap
        self.line_join = line_join
        self.tolerance = tolerance

        super(Shape, self).__init__(x, y, w, h, margin, [e + stroke_width for e in padding], layout)
        
    def stroke_and_fill(self, cr: cairo.Context, w, h):
        if self.dash:
            cr.set_dash(**self.dash)
        if self.line_cap:
            cr.set_line_cap(self.line_cap)
        if self.line_join:
            cr.set_line_join(self.line_join)
        if self.tolerance: # fidelity
            cr.set_tolerance(self.tolerance)
        cr.set_line_width(self.stroke_width)
        if self.fill_src:
            self.fill_src.set(cr, 0, 0, w, h)
            cr.fill_preserve()
        if self.stroke_src:
            self.stroke_src.set(cr, 0, 0, w, h)
            cr.stroke()

        if not self.fill_src and not self.stroke_src:
            warn('This Shape doesn\'t has both fill_src and stroke_src set to None.')


class Line(Shape):

    def __init__(self, x1, y1, x2, y2, stroke_width=3, stroke_src=COLOR_BLACK, dash=None, line_cap=None):
        x = min(x1, x2) - stroke_width / 2
        y = min(y1, y2) - stroke_width / 2
        w = max(x1, x2) - x + stroke_width
        h = max(y1, y2) - y + stroke_width
        
        self.x1 = x1 - x
        self.y1 = y1 - y
        self.x2 = x2 - x
        self.y2 = y2 - y
        
        super(Line, self).__init__(x, y, w, h, stroke_width=stroke_width, stroke_src=stroke_src, dash=dash,
                                   line_cap=line_cap, fill_src=None)

    def _draw(self, surface: cairo.Surface, w, h):
        cr = cairo.Context(surface)

        cr.move_to(self.x1, self.y1)
        cr.line_to(self.x2, self.y2)

        self.stroke_and_fill(cr, w, h)


class Rectangle(Shape):

    def _draw(self, surface: cairo.Surface, w, h):
        cr = cairo.Context(surface)

        x, y, w_shape, h_shape = adjust_rect_size_by_line_width(0, 0, w, h, self.stroke_width)
        cr.rectangle(x, y, w_shape, h_shape)
        
        self.stroke_and_fill(cr, w, h)


class Circle(Shape):

    def __init__(self, x, y, radius, stroke_width=3, padding=(0, 0, 0, 0), **kwargs):
        self.radius = radius

        super(Circle, self).__init__(x, y, 2 * radius, 2 * radius, stroke_width=stroke_width, padding=[e + stroke_width for e in padding], **kwargs)

    def _draw(self, surface: cairo.Surface, w, h):
        cr = cairo.Context(surface)

        x, y, w_shape, h_shape = adjust_rect_size_by_line_width(0, 0, w, h, self.stroke_width)
        
        draw_radius = w_shape / 2
        
        cr.arc(int(x + w_shape / 2), int(y + h_shape / 2), draw_radius, 0, 2 * math.pi)
        
        self.stroke_and_fill(cr, w, h)
        

class RoundedRectangle(Shape):

    def __init__(
            self, x, y, w, h, radius=10, stroke_width=3, stroke_src=COLOR_BLACK,
            fill_src=COLOR_WHITE, layout=None, margin=(0, 0, 0, 0), padding=(0, 0, 0, 0)):
        self.radius = radius

        super(RoundedRectangle, self).__init__(x, y, w, h, stroke_width, stroke_src, fill_src, layout, margin, padding)

    def _draw(self, surface: cairo.Surface, w, h):
        cr = cairo.Context(surface)
        x, y, w_shape, h_shape = adjust_rect_size_by_line_width(0, 0, w, h, self.stroke_width)
        x1, y1, x2, y2 = x, y, x + w_shape, y + h_shape

        cr.arc(x1 + self.radius, y1 + self.radius, self.radius, 2 * (pi / 2), 3 * (pi / 2))
        cr.arc(x2 - self.radius, y1 + self.radius, self.radius, 3 * (pi / 2), 4 * (pi / 2))
        cr.arc(x2 - self.radius, y2 - self.radius, self.radius, 0 * (pi / 2), 1 * (pi / 2))  # ;o)
        cr.arc(x1 + self.radius, y2 - self.radius, self.radius, 1 * (pi / 2), 2 * (pi / 2))
        cr.close_path()

        self.stroke_and_fill(cr, w, h)


# if __name__ == '__main__':
#     c = Rectangle(0, 0, 500, 500, fill_src=COLOR_WHITE, stroke_width=0)
#     # shape = Rectangle(10, 10, 50, 50, dash=dict(dashes=[10, 5], offset=5))
#     # shape = Circle(0, 0, 100, 10, dash=dict(dashes=[10, 5], offset=5), line_cap=cairo.LINE_CAP_BUTT)
#     shape = Line(10, 10, 100, 10, dash={'dashes': [10, 5]})
#     c.add(shape)
#     c.image().show()
