from abc import ABC
from PIL import Image


COLOR_BLACK = (0, 0, 0, 255)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_TRANSPARENT = (0, 0, 0, 0)


class Component(ABC):
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.children = []
    
    def _draw(self, im: Image):
        for child in self.children:
            im_ = Image.new('RGBA', (self.w, self.h), COLOR_TRANSPARENT)
            child._draw(im_)
            im.paste(im_, (self.x, self.y), im_)
    
    def scale(self, val):
        self.x = int(self.x * val)
        self.y = int(self.y * val)
        self.w = int(self.w * val)
        self.h = int(self.h * val)
        
        for child in self.children:
            child.scale(val)

    def image(self):
        im = Image.new('RGBA', (self.w + self.x, self.h + self.y), COLOR_TRANSPARENT)
        self._draw(im)

        return im
    
    def clone(self):
        pass
    
    def add(self, child):
        self.children.append(child)