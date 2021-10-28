from bgfactory.components.constants import COLOR_WHITE
from bgfactory.components.shape import Rectangle


class CardSheet(Rectangle):
    
    def __init__(self, w, h, cards, reversed=False):

        super(CardSheet, self).__init__(0, 0, w, h, 0, fill_src=COLOR_WHITE)
        
        card0 = cards[0]
        for card in cards:
            if (card.w != card0.w or card.h != card0.h):
                raise ValueError('all cards must have the same width and height')
        
        cw, ch = card0.w, card0.h
        
        MIN_PADDING_X = 0.035 * w
        MIN_PADDING_Y = 0.02 * h
        
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
        
    def get_size(self):
        return self.w, self.h