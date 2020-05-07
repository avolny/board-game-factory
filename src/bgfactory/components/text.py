from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw

from bgfactory.components.component import Component
from bgfactory.components.constants import COLOR_BLACK, INFER, COLOR_TRANSPARENT, HALIGN_LEFT, VALIGN_TOP, \
    HALIGN_CENTER, HALIGN_RIGHT, VALIGN_MIDDLE, VALIGN_BOTTOM


class Text(Component):
    
    
    _dummy_image = Image.new('RGBA', (1920, 1080), COLOR_TRANSPARENT)
    
    def __init__(self, x, y, w, h, text, font="FELIXTI.TTF", font_size=50, spacing=15, halign=HALIGN_LEFT,
                 valign=VALIGN_TOP, color=COLOR_BLACK, stroke_width=0, stroke_color=None,
                 yoffset=0, margin=(0,0,0,0)):
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
        
        super(Text, self).__init__(x, y, w, h, margin)
        
    def scale(self, val):
        self.font_size = int(round(self.font_size * val))
        self.spacing = int(round(self.spacing * val))
        self.stroke_width = int(round(self.stroke_width * val))
        
        super(Text, self).scale(val)
        
    def _draw(self, im: Image):
        draw = ImageDraw(im)
        
        w, h = im.size

        wtext, htext = self._get_text_size()
        
        htext += self.yoffset
        
        x = 0
        y = self.yoffset
        
        if (self.halign == HALIGN_CENTER):
            x = int(round(w / 2 - wtext / 2))
        elif (self.halign == HALIGN_RIGHT):
            x = int(round(w - wtext)) + 1
        
        if (self.valign == VALIGN_MIDDLE):
            y = int(round(h / 2 - htext / 2)) + self.yoffset
        if (self.valign == VALIGN_BOTTOM):
            y = int(round(h - htext)) + self.yoffset

        # print(x, y)
            
        draw.text(
            xy=(x, y), text=self.text, fill=self.color, font=self._get_font(), spacing=self.spacing,
            align=self.halign, stroke_width=self.stroke_width, stroke_fill=self.stroke_color
        )
        
    def _get_font(self):
        return ImageFont.truetype(self.font, size=self.font_size, index=0, encoding='unic')
        
    def _get_text_size(self):
        draw = ImageDraw(self._dummy_image)
        
        return draw.multiline_textsize(
            text=self.text, font=self._get_font(), spacing=self.spacing, stroke_width=self.stroke_width)
        
    def get_size(self):
        w, h = self.w, self.h
        tw, th = self._get_text_size()
        
        if w == INFER:
            w = tw
        if h == INFER:
            h = th + self.yoffset
        
        return w, h