from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw

from src.bgfactory.components.component import Component
from src.bgfactory.components.constants import COLOR_BLACK


class Text(Component):
    
    HALIGN_LEFT = 'left'
    HALIGN_CENTER = 'center'
    HALIGN_RIGHT = 'right'
    VALIGN_TOP = 'top'
    VALIGN_MIDDLE = 'middle'
    VALIGN_BOTTOM = 'bottom'
    
    def __init__(self, x, y, w, h, text, font="FELIXTI.TTF", font_size=50, spacing=15, halign=HALIGN_LEFT,
                 valign=VALIGN_TOP, color=COLOR_BLACK, stroke_width=0, stroke_color=None,
                 yoffset=0):
        self.text = text
        self.font = font
        self.font_size = font_size
        self.color = color
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.spacing = spacing
        self.halign = halign
        self.valign = valign
        self.yoffset = yoffset
        
        super(Text, self).__init__(x, y, w, h)
        
    def scale(self, val):
        self.font_size = int(round(self.font_size * val))
        self.spacing = int(round(self.spacing * val))
        self.stroke_width = int(round(self.stroke_width * val))
        
        super(Text, self).scale(val)
        
    def _draw(self, im: Image):
        draw = ImageDraw(im)
        
        w, h = im.size
        
        font = ImageFont.truetype(self.font, size=self.font_size, index=0, encoding='unic')
        
        wtext, htext = draw.multiline_textsize(
            text=self.text, font=font, spacing=self.spacing, stroke_width=self.stroke_width)
        
        x = 0
        y = self.yoffset
        
        if (self.halign == self.HALIGN_CENTER):
            x = int(round(w / 2 - wtext / 2))
        elif (self.halign == self.HALIGN_RIGHT):
            x = int(round(w - wtext)) + 1
        
        if (self.valign == self.VALIGN_MIDDLE):
            y = int(round(h / 2 - htext / 2)) + self.yoffset
        if (self.valign == self.VALIGN_BOTTOM):
            y = int(round(h - htext)) + self.yoffset
            
        draw.text(
            xy=(x, y), text=self.text, fill=self.color, font=font, spacing=self.spacing,
            align=self.halign, stroke_width=self.stroke_width, stroke_fill=self.stroke_color
        )