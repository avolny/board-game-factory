from math import floor
from warnings import warn

import cairocffi as cairo

from bgfactory.common.profiler import profile
from bgfactory.components.component import Container
from bgfactory.components.constants import HALIGN_LEFT, HALIGN_CENTER, HALIGN_RIGHT, INFER, FILL, VALIGN_TOP, \
    VALIGN_MIDDLE, VALIGN_BOTTOM
from bgfactory.components.layout.layout_manager import LayoutManager, LayoutError
from bgfactory.components.shapes import Rectangle
from bgfactory.components.utils import is_percent, parse_percent


class HorizontalFlowLayout(LayoutManager):
    """

    For w,h following applies:

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

        w_margins = 0
        # compute height including margins
        for child in children:
            w_margins += max(prev_margin, child.margin[0])
            prev_margin = child.margin[2]

        w_margins += max(0, prev_margin)

        # compute child dimensions
        w_content = 0
        children_dimensions = []
        for i, child in enumerate(children):

            cw, ch = child.get_size()

            if ch == FILL:
                ch = '100%'
            if cw == FILL:
                if i < len(children) - 1:
                    raise LayoutError("Only the last child can have it's width set to FILL")

                cw = w_padded - w_margins - w_content

            if is_percent(ch):
                ch = parse_percent(ch) * (h_padded - child.margin[1] - child.margin[3])
            if is_percent(cw):
                cw = parse_percent(cw) * (w_padded - w_margins)

            w_content += cw

            children_dimensions.append((cw, ch))

        if w_content > w_padded - w_margins:
            print(w_content)
            print(w_padded)
            print(w_margins)
            warn('Children overflow the width of the layout')

        y = self.parent.padding[0]

        if self.halign == HALIGN_LEFT:
            cx = self.parent.padding[0]
        elif self.halign == HALIGN_CENTER:
            cx = self.parent.padding[0] + (w_padded / 2 - w_margins / 2 - w_content / 2)
        elif self.halign == HALIGN_RIGHT:
            cx = w - self.parent.padding[2] - w_content - w_margins
        else:
            raise ValueError('unrecognized halign: ' + str(self.halign))

        prev_margin = 0
        for child, (cw, ch) in zip(children, children_dimensions):

            if self.valign == VALIGN_TOP:
                cy = y + child.margin[1]
            elif self.valign == VALIGN_MIDDLE:
                cy = y + child.margin[1] + (h_padded - child.margin[1] - child.margin[3]) / 2 - ch / 2
            elif self.valign == VALIGN_BOTTOM:
                cy = y - child.margin[1] + h_padded - ch
            else:
                raise ValueError('unrecognized halign: {}' + str(self.halign))

            cx += max(prev_margin, child.margin[0])
            prev_margin = child.margin[2]

            child_surface = child.draw(floor(cw), floor(ch))

            profile('paint child surface')
            cr.set_source_surface(child_surface, floor(cx), floor(cy))
            cr.paint()
            profile()

            cx += cw

    def get_size(self):
        w, h = None, None

        if self.parent.w != INFER:
            w = self.parent.w

        if self.parent.h != INFER:
            h = self.parent.h

        if (w is not None and h is not None):
            return (w, h)

        max_h = 0
        # infer required dimensions
        # x, y = self.padding[:2]
        x = self.parent.padding[0]

        prev_margin = 0

        for i, child in enumerate(self.parent.children):
            cw, ch = child.get_size()

            if self.parent.w == INFER:
                max_h = max(
                    max_h, ch + self.parent.padding[1] + self.parent.padding[3] + child.margin[1] + child.margin[3])

            if self.parent.h == INFER:
                x += cw + max(prev_margin, child.margin[0])

            prev_margin = child.margin[2]

        x += max(0, prev_margin) + self.parent.padding[2]

        w = x or w or 0
        h = max_h or h or 0

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
                fill_color=(0, 1, 0, 1), padding=(10, 10, 10, 10), layout=HorizontalFlowLayout(halign, valign))

            box1 = Rectangle(
                0, 0, '60%', '60%', stroke_width=2, stroke_color=(0, 0, 0, 1), fill_color=(1, 0, 0, 0.5),
                margin=(5, 5, 5, 5)
            )

            box2 = Rectangle(
                0, 0, '60%', '60%', stroke_width=2, stroke_color=(0, 0, 0, 1), fill_color=(1, 0, 0, 0.5),
                margin=(5, 5, 5, 5)
            )

            card.add(box1)
            card.add(box2)
            rect.add(card)

    rect.image().show()
    # card.image().save('output/test_vertflow.png')