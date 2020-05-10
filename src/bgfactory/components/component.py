from abc import ABC, abstractmethod
from math import ceil

import cairocffi as cairo

from bgfactory.components.cairo_helpers import image_from_surface
from bgfactory.components.constants import FILL
from bgfactory.components.layout_manager import AbsoluteLayout
from bgfactory.common.profiler import profile


class Component(ABC):
    
    def __init__(self, x, y, w, h, margin=(0, 0, 0, 0)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.margin = margin
        
        if self.w == FILL:
            raise NotImplementedError()
        if self.h == FILL:
            raise NotImplementedError()

    @abstractmethod
    def draw(self, w, h):
        profile('cairo.ImageSurface')
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(ceil(w)), int(ceil(h)))
        profile()
        
        return surface
    
    def image(self):
        return image_from_surface(self.draw(self.w, self.h))
    
    @abstractmethod
    def get_size(self):
        pass
    
        
class Container(Component):
    
    def __init__(self, x, y, w, h, margin=(0, 0, 0, 0), padding=(0, 0, 0, 0), layout=None):

        self.children = []

        if layout is None:
            self.layout = AbsoluteLayout()
        else:
            self.layout = layout
        
        self.padding = padding
        self.layout.set_parent(self)

        super(Container, self).__init__(x, y, w, h, margin)
    
    def get_size(self):
        return self.layout.get_size()
    
    def add(self, child):
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
        
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        
        self._draw(surface, w, h)
        self.layout._draw(surface, w, h)
        
        return surface