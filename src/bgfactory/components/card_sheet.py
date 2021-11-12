from bgfactory.components.constants import COLOR_WHITE, INFER
from bgfactory.components.shape import Rectangle, Line
from bgfactory.components.text import TextUniform, FontDescription


class CardSheet(Rectangle):
    
    def __init__(self, w, h, cards, reversed=False, cutlines=True, page=None):

        super(CardSheet, self).__init__(0, 0, w, h, 0, fill_src=COLOR_WHITE)

        self.cutlines = cutlines
        
        card0 = cards[0]
        for card in cards:
            if (card.w != card0.w or card.h != card0.h):
                raise ValueError('all cards must have the same width and height')
        
        cw, ch = card0.w, card0.h
        
        MIN_PADDING_X = 0.02 * min(w, h)
        MIN_PADDING_Y = 0.02 * min(w, h)
        
        self.ncols = int((w - MIN_PADDING_X * 2) // cw)
        self.nrows = int((h - MIN_PADDING_Y * 2) // ch)
        
        padx = (w - self.ncols * cw) // 2
        pady = (h - self.nrows * ch) // 2
        
        # print(padx, pady)
        # print(h, ch)
        # print(nrows)
        
        for i in range(self.nrows):
            for j in range(self.ncols):
                index = i * self.ncols + j
                if (index < len(cards)):
                    card = cards[index]
                    
                    if reversed:
                        card.x = self.w - padx - (j + 1) * cw
                    else:
                        card.x = padx + j * cw
                    card.y = pady + i*ch
                    self.add(card)
                    
        if page:
            self.add(TextUniform(w * 0.9, h - pady * 0.7, INFER, INFER, str(page), FontDescription(size=min(50, pady * 0.4))))
                    
        if cutlines:
            pad_outside = 35
            pad_inside = 15
            for i in range(self.nrows + 1):
                self.add(Line(pad_outside, pady + ch * i, padx - pad_inside, pady + ch * i, 
                              stroke_width=2, dash={'dashes': [10, 5]}))
                self.add(Line(w - padx + pad_inside, pady + ch * i, w - pad_outside, pady + ch * i,
                              stroke_width=2, dash={'dashes': [10, 5]}))
                
            for i in range(self.nrows + 1):
                self.add(Line(padx + cw * i, pad_outside, padx + cw * i, pady - pad_inside, 
                              stroke_width=2, dash={'dashes': [10, 5]}))
                self.add(Line(padx + cw * i, h - pady + pad_inside, padx + cw * i, h - pad_outside,
                              stroke_width=2, dash={'dashes': [10, 5]}))
        
    def get_size(self):
        return self.w, self.h