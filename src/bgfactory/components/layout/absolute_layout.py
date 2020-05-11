import cairocffi as cairo

from bgfactory.common.profiler import profile
from bgfactory.components.constants import INFER, FILL
from bgfactory.components.layout.layout_manager import LayoutManager, LayoutError
from bgfactory.components.utils import is_percent, parse_percent


class AbsoluteLayout(LayoutManager):
    """
    The default LayoutManager for every component
    
    for both w and h following applies:
        - if parent dimension is INFER, child dimension and location can only be pixels
        - if parent dimension is not INFER, child dimension and location can be pixels or percentage
        
    """
    
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

    def _draw(self, surface: cairo.Surface, w, h):
        
        cr = cairo.Context(surface)
        
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
            
            child_surface = child.draw(cw, ch)

            # im_ = child.image(cw, ch)
            # child._draw(im_)
            
            profile('paint child surface')
            cr.set_source_surface(child_surface, cx, cy)
            cr.paint()
            profile()