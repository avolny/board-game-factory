from abc import ABC, abstractmethod

from PIL import Image

from bgfactory.components.constants import COLOR_TRANSPARENT, FILL
from bgfactory.components.layout_manager import AbsoluteLayout


class Component(ABC):
    
    
    def __init__(self, x, y, w, h, margin=(0,0,0,0)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.margin = margin
        
        if w == FILL:
            raise NotImplementedError()
        if h == FILL:
            raise NotImplementedError()

    @abstractmethod
    def _draw(self, im: Image):
        pass
    
    def _mask(self):
        return Image.new('RGBA', (self.w, self.h), COLOR_TRANSPARENT)
    
    def scale(self, val):
        if isinstance(self.x, int):
            self.x = int(self.x * val)
        if isinstance(self.y, int):
            self.y = int(self.y * val)
        if isinstance(self.w, int):
            self.w = int(self.w * val)
        if isinstance(self.h, int):
            self.h = int(self.h * val)

        self.margin = [int(round(e * val)) for e in self.margin]

    def image(self, w=None, h=None):
        if w is None:
            w = self.w
        if h is None:
            h = self.h
            
        im = Image.new('RGBA', (w, h), COLOR_TRANSPARENT)
        self._draw(im)

        return im
    
    @abstractmethod
    def get_size(self):
        pass
    
    def clone(self):
        pass
        
        
class Container(Component):
    
    def __init__(self, x, y, w, h, margin=(0,0,0,0), padding=(0, 0, 0, 0), layout=None):

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
    
    def _draw(self, im):
        self.layout._draw(im)
        
    def scale(self, val):
        for child in self.children:
            child.scale(val)
            
        self.padding = [int(round(e * val)) for e in self.padding]
            
        super(Container, self).scale(val)