from abc import ABC, abstractmethod

from PIL import Image

from src.bgfactory.components.utils import parse_percent, is_percent
from src.bgfactory.components.constants import INFER, FILL


class LayoutError(ValueError):
    pass


class LayoutManager(ABC):
    
    def __init__(self):
        pass
    
    def set_parent(self, parent):
        self.parent = parent
    
    @abstractmethod
    def _draw(self, im: Image):
        pass
    
    @abstractmethod
    def get_size(self):
        pass
    
    @abstractmethod
    def validate_child(self, child):
        pass
    
    
class AbsoluteLayout(LayoutManager):
    """
    The default LayoutManager for every component
    
    for both w and h following applies:
        - if parent dimension is INFER, child dimension and location can only be pixels
        - if parent dimension is not INFER, child dimension and location can be pixels or percentage
        
    """
    
    def __init__(self):
        pass
    
    def get_size(self):
        w, h = None, None
        
        if self.parent.w != INFER:
            w = self.parent.w
            
        if self.parent.h != INFER:
            h = self.parent.h
        
        if (w is not None and h is not None):
            return (w, h)
        
        max_w, max_h = 0, 0 
        # infer required dimensions
        for i, child in enumerate(self.parent.children):
            cw, ch = child.get_size()
            cx = child.x
            cy = child.y
            
            if w == INFER:
                max_w = max(max_w, cw + cx)
                
            if h == INFER:
                max_h = max(max_h, ch + cy) 
                
        w = max_w or w
        h = max_h or h
        
        return w, h
    
    def validate_child(self, child):
        if child.w == FILL:
            raise LayoutError('width="fill" is not allowed')
        if child.h == FILL:
            raise LayoutError('height="fill" is not allowed')
        if self.parent.w == INFER and is_percent(child.w):
            raise LayoutError('width="n%" is not allowed when parent width=="infer"')
        if self.parent.h == INFER and is_percent(child.h):
            raise LayoutError('height="n%" is not allowed when parent height=="infer"')

    def _draw(self, im: Image):
        w, h = im.size
        
        for child in self.parent.children:
            # im_ = Image.new('RGBA', (self.w, self.h), COLOR_TRANSPARENT)
            
            cw, ch = child.get_size()
            
            if is_percent(cw):
                cw = int(parse_percent(cw) * w)
            if is_percent(ch):
                ch = int(parse_percent(ch) * h)
                
            cx, cy = child.x, child.y
            
            if is_percent(cx):
                cx = int(parse_percent(cx) * w)
            if is_percent(cy):
                cy = int(parse_percent(cy) * h)
            
            im_ = child.image(cw, ch)
            im.paste(im_, (cx, cy), im_)
    
    
class FlowLayoutHorizontal(LayoutManager):
    
    def __init__(self, padding=(5,5)):
        """
        :param padding: (left, top) 
        """
        self.padding = padding
        
    def get_size(self):
        w, h = None, None

        if self.parent.w != INFER:
            w = self.parent.w

        if self.parent.h != INFER:
            h = self.parent.h
        
    def _draw(self, im: Image):
        children = self.parent.children
        
        x, y = self.padding[:2]
        for child in children:
            im_ = child.draw_(im)
            im.paste(im_, (x, y), im_)
            
            x += im_.size[0] + self.padding[0] + self.padding[2]


class FlowLayoutVertical(LayoutManager):
    def __init__(self, padding=(5, 5)):
        """
        :param padding: (left, top) 
        """
        self.padding = padding

    def _draw(self, im: Image):
        children = self.parent.children

        x, y = self.padding[:2]
        for child in children:
            im_ = child.draw_(im)
            im.paste(im_, (x, y), im_)

            x += im_.size[0] + self.padding[0] + self.padding[2]