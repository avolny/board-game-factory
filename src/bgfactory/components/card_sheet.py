from bgfactory.components.constants import COLOR_WHITE
from bgfactory.components.shape import Rectangle


class CardSheet(Rectangle):
    
    def __init__(self, w, h, cards):

        super(CardSheet, self).__init__(0, 0, w, h, 0, fill_src=COLOR_WHITE)
        
        card0 = cards[0]
        for card in cards:
            if (card.w != card0.w or card.h != card0.h):
                raise ValueError('all cards must have the same width and height')
        
        cw, ch = card0.w, card0.h
        
        MIN_PADDING_X = 0.005 * w
        MIN_PADDING_Y = 0.005 * h
        
        ncols = int((w - MIN_PADDING_X * 2) // cw)
        nrows = int((h - MIN_PADDING_Y * 2) // ch)
        
        padx = (w - ncols * cw) // 2
        pady = (h - nrows * ch) // 2
        
        for i in range(nrows):
            for j in range(ncols):
                index = i * ncols + j
                if (index < len(cards)):
                    card = cards[index]
                    
                    card.x = padx + j*cw
                    card.y = pady + i*ch
                    self.add(card)
        
    def get_size(self):
        return self.w, self.h