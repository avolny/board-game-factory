from math import floor
from warnings import warn

import cairocffi as cairo

from bgfactory.common.profiler import profile
from bgfactory.components.component import Container
from bgfactory.components.constants import HALIGN_LEFT, HALIGN_CENTER, HALIGN_RIGHT, INFER, FILL, VALIGN_TOP, \
    VALIGN_MIDDLE, VALIGN_BOTTOM
from bgfactory.components.layout.layout_manager import LayoutManager, LayoutError
from bgfactory.components.shape import Rectangle
from bgfactory.components.utils import is_percent, parse_percent


class VerticalFlowLayout(LayoutManager):
    """

    For w, h following applies:

    If parent.w==INFER, child.w in [px]
    If parent.w!=INFER, child.w in [px, n%]
    If parent.h==INFER, child.h in [px]
    If parent.h!=INFER, child.h in [px, n%]
    """

    def __init__(self, halign=HALIGN_LEFT, valign=VALIGN_TOP):
        """
        :param padding: (left, top, right, bottom) 
        """
        self.halign = halign
        self.valign = valign

    def _draw(self, surface: cairo.Surface, w, h):

        cr = cairo.Context(surface)

        children = self.parent.children
        w_padded = w - self.parent.padding[0] - self.parent.padding[2]
        h_padded = h - self.parent.padding[1] - self.parent.padding[3]

        prev_margin = 0
        
        h_margins = 0
        # compute height including margins
        for child in children:
            h_margins += max(prev_margin, child.margin[1])
            prev_margin = child.margin[3]

        h_margins += max(0, prev_margin)

        # compute child dimensions
        h_content = 0 
        children_dimensions = []
        for i, child in enumerate(children):
            
            cw, ch = child.get_size()

            if cw == FILL:
                cw = '100%'
            if ch == FILL:
                if i < len(children) - 1:
                    raise LayoutError("Only the last child can have it's height set to FILL")
                
                ch = h_padded - h_margins - h_content

            if is_percent(cw):
                cw = parse_percent(cw) * (w_padded - child.margin[0] - child.margin[2])
            if is_percent(ch):
                ch = parse_percent(ch) * (h_padded - h_margins)
                
            h_content += ch
            
            children_dimensions.append((cw, ch))

        if h_content > h_padded - h_margins:
            print(h_content)
            print(h_padded)
            print(h_margins)
            warn('Children overflow the height of the layout')
            
        # remainder_h_content = max(remainder_h_content, 0)

        x = self.parent.padding[0]
        
        if self.valign == VALIGN_TOP:
            cy = self.parent.padding[1]
        elif self.valign == VALIGN_MIDDLE:
            cy = self.parent.padding[1] + (h_padded / 2 - h_margins / 2 - h_content / 2)
        elif self.valign == VALIGN_BOTTOM:
            cy = h - self.parent.padding[3] - h_content - h_margins
        else:
            raise ValueError('unrecognized valign: ' + str(self.valign))
        
        prev_margin = 0
        for child, (cw, ch) in zip(children, children_dimensions):

            if self.halign == HALIGN_LEFT:
                cx = x + child.margin[0]
            elif self.halign == HALIGN_CENTER:
                cx = x + child.margin[0] + (w_padded - child.margin[0] - child.margin[2]) / 2 - cw / 2
            elif self.halign == HALIGN_RIGHT:
                cx = x - child.margin[0] + w_padded - cw
            else:
                raise ValueError('unrecognized halign: {}' + str(self.halign))

            cy += max(prev_margin, child.margin[1])
            prev_margin = child.margin[3]

            child_surface = child.draw(floor(cw), floor(ch))

            profile('paint child surface')
            cr.set_source_surface(child_surface, floor(cx), floor(cy))
            cr.paint()
            profile()

            cy += ch

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
        if self.parent.w == INFER and child.w == FILL:
            raise LayoutError('width="fill" is not allowed when parent width=="infer"')
        if self.parent.h == INFER and child.h == FILL:
            raise LayoutError('height="fill" is not allowed when parent height=="infer"')
        if self.parent.w == INFER and (is_percent(child.w) or is_percent(child.x)):
            raise LayoutError('width="n%" or x="n%" is not allowed when parent width=="infer"')
        if self.parent.h == INFER and (is_percent(child.h) or is_percent(child.y)):
            raise LayoutError('height="n%" or y="n%" is not allowed when parent height=="infer"')
        
        
if __name__ == '__main__':
    
    
    rect = Container(0, 0, 600, 600)
    
    haligns = [HALIGN_LEFT, HALIGN_CENTER, HALIGN_RIGHT]
    valigns = [VALIGN_TOP, VALIGN_MIDDLE, VALIGN_BOTTOM]
    
    for i, halign in enumerate(haligns):
        for j, valign in enumerate(valigns):
            
            card = Rectangle(
                i * 200, j * 200, 200, 200, stroke_width=5, stroke_color=(1, 0, 0, 1),
                fill_color=(0, 1, 0, 1), padding=(10, 10, 10, 10), layout=VerticalFlowLayout(halign, valign))
        
            box1 = Rectangle(
                0, 0, 40, 20, stroke_width=2, stroke_color=(0, 0, 0, 1), fill_color=(1, 0, 0, 0.5),
                margin=(5, 5, 5, 5)
            )
            
            box2 = Rectangle(
                0, 0, '50%', 30, stroke_width=2, stroke_color=(0, 0, 0, 1), fill_color=(1, 0, 0, 0.5),
                margin=(5, 5, 5, 5)
            )
        
            card.add(box1)
            card.add(box2)
            rect.add(card)
            
    rect.image().show()
    # card.image().save('output/test_vertflow.png')