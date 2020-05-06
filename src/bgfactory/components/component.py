from abc import ABC, abstractmethod

from PIL import Image

from src.bgfactory.components.constants import COLOR_TRANSPARENT
from src.bgfactory.components.layout_manager import AbsoluteLayout


class Component(ABC):
    
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    @abstractmethod
    def _draw(self, im: Image):
        pass
    
    def _mask(self):
        return Image.new('RGBA', (self.w, self.h), COLOR_TRANSPARENT)
    
    def scale(self, val):
        self.x = int(self.x * val)
        self.y = int(self.y * val)
        self.w = int(self.w * val)
        self.h = int(self.h * val)
        
        for child in self.children:
            child.scale(val)

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
    
    def __init__(self, x, y, w, h, layout=None):

        self.children = []

        if layout is None:
            self.layout = AbsoluteLayout()
        else:
            self.layout = layout

        self.layout.set_parent(self)

        super(Container, self).__init__(x, y, w, h)
    
    def get_size(self):
        return self.layout.get_size()
    
    def add(self, child):
        self.layout.validate_child(child)
        self.children.append(child)
    
    def _draw(self, im):
        self.layout._draw(im)