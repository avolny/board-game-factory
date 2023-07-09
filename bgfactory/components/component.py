from abc import ABC, abstractmethod
from math import ceil
from warnings import warn

import cairocffi as cairo

from bgfactory.components.cairo_helpers import image_from_surface
from bgfactory.components.constants import FILL
from bgfactory.components.layout.absolute_layout import AbsoluteLayout
from bgfactory.common.profiler import profile

DEBUG = False
# DEBUG = True

class Component(ABC):
    
    def __init__(self, x, y, w, h, margin=(0, 0, 0, 0)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.margin = margin

    @abstractmethod
    def draw(self, w, h):
        profile('cairo.ImageSurface')
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(ceil(w)), int(ceil(h)))
        profile()
        if DEBUG:
            cr = cairo.Context(surface)
            cr.rectangle(0, 0, int(ceil(w)), int(ceil(h)))
            cr.set_source_rgba(0.7, 0.3, 0.2, 0.5)
            cr.set_line_width(3)
            cr.stroke()
        
        return surface
    
    def image(self):
        w, h = self.get_size()        
        return image_from_surface(self.draw(w, h))
    
    @abstractmethod
    def get_size(self):
        pass
    
        
class Container(Component):
    
    def __init__(self, x, y, w, h, margin=(0, 0, 0, 0), padding=(0, 0, 0, 0), layout=None, children=None):

        if layout is None:
            self.layout = AbsoluteLayout()
        else:
            self.layout = layout

        self.padding = padding
        self.layout.set_parent(self)

        super(Container, self).__init__(x, y, w, h, margin)

        if children is None:
            self.children = []
        else:
            if not isinstance(children, (list, tuple)):
                raise TypeError(f'children must be list or tuple but is {type(children)=}')
            self.children = list(children)

            for child in self.children:
                self.layout.validate_child(child)
    
    def get_size(self):
        return self.layout.get_size()    
    
    def add(self, child, *other_children):
        self.layout.validate_child(child)
        self.children.append(child)

        for child in other_children:
            self.layout.validate_child(child)
            self.children.append(child)

        
    def _draw(self, surface, w, h):
        """
        Override this method for drawing under the Container's children
        :param surface: surface to draw on
        :return:
        """
        pass
    
    def draw(self, w, h):

        surface = super(Container, self).draw(w, h)
        # surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w), int(h))
        
        self._draw(surface, w, h)
        self.layout._draw(surface, w, h)
        
        return surface