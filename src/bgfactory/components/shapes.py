from PIL import Image
from PIL import ImageDraw
from PIL.ImageDraw import floodfill

import src.bgfactory.pil_patch.rounded_rectangle

from src.bgfactory.components.component import Component, COLOR_TRANSPARENT, COLOR_WHITE, COLOR_BLACK


class Shape(Component):
    
    def __init__(self, x, y, w, h, stroke_width=3, stroke_color=COLOR_BLACK, fill_color=COLOR_WHITE):
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        
        super(Shape, self).__init__(x, y, w, h)
    
    def scale(self, val):
        self.stroke_width = int(self.stroke_width * val)
        super(Shape, self).scale(val)
        

class Rectangle(Shape):
    
    def _draw(self, im: Image):
        draw = ImageDraw.Draw(im)
        
        draw.rectangle(((self.x, self.y), (self.x + self.w - 1, self.y + self.h - 1)), 
                       outline=self.stroke_color, width=self.stroke_width, fill=self.fill_color)
        
        super(Rectangle, self)._draw(im)


class RoundedRectangle(Shape):
    
    
    def __init__(self, x, y, w, h, radius=10, stroke_width=3, stroke_color = COLOR_BLACK, fill_color = COLOR_WHITE):
        self.radius = radius
        
        super(RoundedRectangle, self).__init__(x, y, w, h, stroke_width, stroke_color, fill_color)
        
    def scale(self, val):
        self.radius = int(self.radius * val)
        super(Shape, self).scale(val)
    
    def _draw(self, im: Image):
        draw = ImageDraw.Draw(im)

        draw.rounded_rectangle(((self.x, self.y), (self.x + self.w - 1, self.y + self.h - 1)),
                       corner_radius=self.radius, outline=self.stroke_color, width=self.stroke_width)
        floodfill(im, (int((self.x + self.x + self.w - 1) / 2), int((self.y + self.y + self.h - 1) / 2)), self.fill_color)

        super(RoundedRectangle, self)._draw(im)


class Ellipse(Shape):
    def _draw(self, im: Image):
        draw = ImageDraw.Draw(im)

        draw.rectangle(((self.x, self.y), (self.x + self.w - 1, self.y + self.h - 1)),
                       outline=self.stroke_color, width=self.stroke_width, fill=self.fill_color)

        super(Ellipse, self)._draw(im)