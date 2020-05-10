from abc import ABC, abstractmethod

from PIL import Image

from bgfactory.components.utils import parse_percent, is_percent
from bgfactory.components.constants import INFER, FILL, HALIGN_LEFT, HALIGN_CENTER, HALIGN_RIGHT
from bgfactory.profiler import profile


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
            
            if self.parent.w == INFER:
                max_w = max(max_w, cw + cx)
                
            if self.parent.h == INFER:
                max_h = max(max_h, ch + cy) 
        
        w = max_w or w or 0
        h = max_h or h or 0
        
        return w, h
    
    def validate_child(self, child):
        if child.w == FILL:
            raise LayoutError('width="fill" is not allowed')
        if child.h == FILL:
            raise LayoutError('height="fill" is not allowed')
        if self.parent.w == INFER and (is_percent(child.w) or is_percent(child.x)):
            raise LayoutError('width="n%" or x="n%" is not allowed when parent width=="infer"')
        if self.parent.h == INFER and (is_percent(child.h) or is_percent(child.y)):
            raise LayoutError('height="n%" or y="n%" is not allowed when parent height=="infer"')

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

            # im_ = child.image(cw, ch)
            # child._draw(im_)
            
            profile('AbsoluteLayout.alpha_composite')
            im__ = Image.new('RGBA', im.size)
            im__.paste(im_, (cx, cy))
            im.paste(Image.alpha_composite(im, im__), (0, 0))
            profile()
    

# class FlowLayoutHorizontal(LayoutManager):
#     
#     def __init__(self, padding=(5,5)):
#         """
#         :param padding: (left, top) 
#         """
#         self.padding = padding
#         
#     def get_size(self):
#         w, h = None, None
# 
#         if self.parent.w != INFER:
#             w = self.parent.w
# 
#         if self.parent.h != INFER:
#             h = self.parent.h
#         
#     def _draw(self, im: Image):
#         children = self.parent.children
#         
#         x, y = self.padding[:2]
#         for child in children:
#             im_ = child.draw_(im)
#             im.paste(im_, (x, y), im_)
#             
#             x += im_.size[0] + self.padding[0] + self.padding[2]


class VerticalFlowLayout(LayoutManager):
    """
    
    For w following applies:
    
    If parent.w==INFER, child.w in [px]
    If parent.w!=INFER, child.w in [px, n%]
    If parent.h==INFER, child.h in [px]
    If parent.h!=INFER, child.h in [px, n%]
    """
    
    def __init__(self, halign=HALIGN_LEFT):
        """
        :param padding: (left, top, right, bottom) 
        """
        self.halign = halign

    def _draw(self, im: Image):
        children = self.parent.children
        w, h = im.size
        w_adj = w - self.parent.padding[0] - self.parent.padding[2]
        h_adj = h - self.parent.padding[1] - self.parent.padding[3]

        x, y = self.parent.padding[:2]
        
        prev_margin = 0
        
        # compute height including margins
        for child in children:
            h_adj -= max(prev_margin, child.margin[1])
            prev_margin = child.margin[3]
            
        h_adj -= max(0, prev_margin)
        
        prev_margin = 0
        for child in children:
            
            cw, ch = child.get_size()
            
            if is_percent(cw):
                cw = int(round(parse_percent(cw) * (w_adj - child.margin[0] - child.margin[2])))
            if is_percent(ch):
                ch = int(round(parse_percent(ch) * h_adj))
            
            cw = min(cw, w_adj)
            
            if self.halign == HALIGN_LEFT:
                x_ = x + child.margin[0]
            elif self.halign == HALIGN_CENTER:
                x_ = x + child.margin[0] + int(round(w_adj / 2 - cw / 2)) 
            elif self.halign == HALIGN_RIGHT:
                x_ = x + child.margin[0] + w_adj - cw
                
            y += max(prev_margin, child.margin[1])
            prev_margin = child.margin[3] 
            
            im_ = child.image(cw, ch)
            # child._draw(im_)

            profile('VerticalFlowLayout.alpha_composite')
            im__ = Image.new('RGBA', im.size)
            im__.paste(im_, (x_, y))
            
            im.paste(Image.alpha_composite(im, im__), (0, 0))
            profile()

            y += ch

    def get_size(self):
        w, h = None, None

        if self.parent.w != INFER:
            w = self.parent.w

        if self.parent.h != INFER:
            h = self.parent.h

        if (w is not None and h is not None):
            return (w, h)

        max_w = 0
        # infer required dimensions
        # x, y = self.padding[:2]
        y = self.parent.padding[1]
        
        prev_margin = 0
        
        for i, child in enumerate(self.parent.children):
            cw, ch = child.get_size()

            if self.parent.w == INFER:
                max_w = max(
                    max_w, cw + self.parent.padding[0] + self.parent.padding[2] + child.margin[0] + child.margin[2])

            if self.parent.h == INFER:
                y += ch + max(prev_margin, child.margin[1])
                
            prev_margin = child.margin[3]
            
        y += max(0, prev_margin) + self.parent.padding[3]
        
        
        w = max_w or w or 0
        h = y or h or 0

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