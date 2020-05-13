from abc import abstractmethod
from typing import Mapping
from warnings import warn

from xml.etree import ElementTree

import cairocffi as cairo
import pangocffi as pango
import pangocairocffi as pc

from bgfactory.components.component import Component
from bgfactory.components.constants import COLOR_BLACK, INFER, HALIGN_LEFT, VALIGN_TOP, \
    HALIGN_CENTER, HALIGN_RIGHT, VALIGN_MIDDLE, VALIGN_BOTTOM
from bgfactory.components.shape import Rectangle
from bgfactory.components.pango_helpers import PANGO_SCALE, convert_to_pango_align, convert_extents
from bgfactory.common.profiler import profile
from bgfactory.components.source import convert_source


class FontDescription():
    
    def __init__(
            self,
            family="Arial",
            size=12,
            weight=pango.Weight.NORMAL,
            style=pango.Style.NORMAL,
            stretch=pango.Stretch.NORMAL,
            gravity=pango.Gravity.AUTO):
        
        self._desc = pango.FontDescription()
        self._desc.set_family(family)
        self._desc.set_absolute_size(size * PANGO_SCALE)
        self._desc.set_weight(weight)
        self._desc.set_style(style)
        self._desc.set_stretch(stretch)
        self._desc.set_gravity(gravity)
    
    def get_pango_font_description(self):
        return self._desc


class _TextComponent(Component):

    def __init__(self, x, y, w, h, text, halign, valign, yoffset, margin):

        self.text = text
        self.yoffset = yoffset
        self.halign = halign
        self.valign = valign
        
        super(_TextComponent, self).__init__(x, y, w, h, margin)

    @abstractmethod
    def _get_text_size(self, w, h):
        pass

    def get_size(self):
        w, h = self.w, self.h
        
        fw, fh = None, None
        if isinstance(w, (int, float)):
            fw = w
        if isinstance(h, (int, float)):
            fw = h

        # substitute in the dimensions that are known to infer the unknown ones
        _, _, tw, th = self._get_text_size(fw, fh)

        if w == INFER:
            w = tw
        if h == INFER:
            h = th + self.yoffset
        
        return w, h
    
    @abstractmethod
    def _draw(self, surface, x, y, w, h):
        pass
    
    def draw(self, w, h):

        surface = super(_TextComponent, self).draw(w, h)

        xoffset, yoffset, wtext, htext = self._get_text_size(w, h)
        
        if htext > h:
            warn('The text contents are higher than the display area, expect some text to be cut off. '
                 'In general to avoid this, avoid using FILL or "n%" on width while using INFER on height of this element. '
                 'When computing the height, the FILL or percentage width is not taken into account and any extra text '
                 'will get cutoff')

        htext += self.yoffset

        x = -xoffset
        y = self.yoffset - yoffset
        
        # print(w, h)

        if (self.halign == HALIGN_CENTER):
            x = w / 2 - (wtext) / 2 - xoffset
        elif (self.halign == HALIGN_RIGHT):
            x = w - wtext - xoffset

        if (self.valign == VALIGN_MIDDLE):
            y = h / 2 - htext / 2 + self.yoffset - yoffset
        if (self.valign == VALIGN_BOTTOM):
            y = h - htext + self.yoffset - yoffset
            
        # print(self.halign, self.valign, x, y, xoffset, yoffset, wtext, htext)
        
        self._draw(surface, x, y, w, h)
        
        return surface


class TextMarkup(_TextComponent):
    """
    Text component that uses the pango markup to define the text appearance,
    see https://developer.gnome.org/pygtk/stable/pango-markup-language.html for the markup language.
    
    You can escape reserved characters like in html/xml e.g &amp; &lt; &gt;
    """
    dummy_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)

    def __init__(self, x, y, w, h, text, font_desc, spacing=3, halign=HALIGN_LEFT,
                 valign=VALIGN_TOP, yoffset=0, text_replace_map: Mapping[str, Component]=None, margin=(0, 0, 0, 0)):
        """
        Initialize Text component that uses pango markup 
        (see https://developer.gnome.org/pygtk/stable/pango-markup-language.html).
        
        Allows also to replace characters by custom glyphs to insert any custom icons naturally into the flow
        of text.
        
        :param x: 
        :param y: 
        :param w: 
        :param h: 
        :param text: markup text 
        :param spacing: number of pixels between lines
        :param halign: horizontal align
        :param valign: vertical align
        :param yoffset: additional yoffset of the text
        :param text_replace_map: dictionary that maps characters onto Components. The component is placed
         vertically on the baseline and horizontally to the middle of the replaced glyph extents. 
         The component.x and component.y values are used as additional offset, this allows for fine-tuned adjustments.
         Note that you have to match the components to the font size yourself.

        :param margin: 
        """
        
        self.spacing = spacing
        if text_replace_map is None:
            text_replace_map = dict()
        self.text_replace_map = text_replace_map
        self.font_desc = font_desc
        
        super(TextMarkup, self).__init__(x, y, w, h, text, halign, valign, yoffset, margin)
        
    def _draw(self, surface, x, y, w, h):
        cr = cairo.Context(surface)

        pc_layout = self._get_pc_layout(cr, w, h)

        profile('text.draw')

        cr.move_to(x, y)
        pc.update_layout(cr, pc_layout)
        pc.show_layout(cr, pc_layout)
        if self.text_replace_map:
            self._draw_glyph_replacements(cr, pc_layout, x, y)
        
        profile()
        
    def _draw_glyph_replacements(self, cr, pc_layout, base_x, base_y):
        # This method might not work on languages that do not flow from left to right 
        
        """
        Order of enumeration

        The iterator works with text which was already reordered by lower level funcs into "visual order". 
        Lines are divided into runs, which are divided into clusters. Each cluster is composed of a sequence of glyphs, 
        and corresponds to a specific sub-sequence of the original text string (in many cases, each glyph corresponds 
        to a single character, but this is not always the case). You should note that the basic unit of reordering is
        the cluster - not character or glyph. A cluster is composed of a 'base-character', and zero or more 
        'combining marks' (in Hebrew and Arabic these are usually 'points'). The points are rendered 
        above/below/inside the base character, so they all have the same logical extents, 
        and no natural "visual" ordering.
         
        :param cr: 
        :param pc_layout: 
        :param base_x: 
        :param base_y: 
        :return: 
        """
        
        layout_iter = pc_layout.get_iter()
        
        text = self._xml_to_plaintext(self.text)
        
        if not text:
            return
        
        char_index = 0
        
        while True:
            
            char = text[char_index]
            ext = layout_iter.get_char_extents()
            y_baseline = base_y + layout_iter.get_baseline() / PANGO_SCALE
            x, y, w, h = base_x + ext.x / PANGO_SCALE, base_y + ext.y / PANGO_SCALE, ext.width / PANGO_SCALE, ext.height / PANGO_SCALE
            
            if char in self.text_replace_map:
                # print(layout_iter.get_index())
                # print(x, y, w, h)
                
                glyph = self.text_replace_map[char]
                
                cr.save()
                # clear out the glyph area
                cr.move_to(x, y)
                cr.rectangle(x, y, w, h)
                cr.set_operator(cairo.OPERATOR_CLEAR)
                cr.fill()
                cr.restore()

                surface = glyph.draw(glyph.w, glyph.h)
                
                # place the glyph on the line baseline to the middle of the removed glyph,
                # the glyph x,y coordinates are used as an offset
                x_glyph = x + w / 2 - glyph.w / 2 + glyph.x
                y_glyph = y_baseline - glyph.h + glyph.y
                
                cr.set_source_surface(surface, x_glyph, y_glyph)
                cr.paint()
            
            char_index += 1
            
            if not layout_iter.next_char():
                break

    def _get_pc_layout(self, cr, w, h):
        pc_layout = pc.create_layout(cr)
        if w is not None:
            pc_layout.set_width(w * PANGO_SCALE)
        pc_layout.set_font_description(self.font_desc._desc)
        pc_layout.set_markup(self.text)
        pc_layout.set_spacing(self.spacing)
        pc_layout.set_alignment(convert_to_pango_align(self.halign))

        return pc_layout

    def _get_text_size(self, w, h):
        cr = cairo.Context(TextUniform.dummy_surface)
        pc_layout = self._get_pc_layout(cr, w, h)

        ink, logical = pc_layout.get_extents()

        # print(ink.x / PANGO_SCALE, ink.y / PANGO_SCALE, ink.width / PANGO_SCALE, ink.height / PANGO_SCALE)
        # print(logical.x / PANGO_SCALE, logical.y / PANGO_SCALE, logical.width / PANGO_SCALE, logical.height / PANGO_SCALE)

        return ink.x / PANGO_SCALE, logical.y / PANGO_SCALE, ink.width / PANGO_SCALE, logical.height / PANGO_SCALE

    def _xml_to_plaintext(self, text):
        return ''.join(ElementTree.fromstring('<root>' + text + '</root>').itertext())
    
    
class TextUniform(_TextComponent):
    """
    A basic Text component that assumes uniform text style. Allows for text outline,
    for making pretty titles etc.
    """
    dummy_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
    
    def __init__(self, x, y, w, h, text, font_description=FontDescription(), spacing=3, halign=HALIGN_LEFT,
                 valign=VALIGN_TOP, fill_src=COLOR_BLACK, stroke_width=0, stroke_src=None,
                 outline_line_join=cairo.LINE_JOIN_MITER, yoffset=0, margin=(0,0,0,0)):
        
        self.font_description = font_description
        self.fill_src = convert_source(fill_src)
        self.stroke_width = stroke_width
        self.stroke_src = convert_source(stroke_src)
        self.spacing = spacing * PANGO_SCALE
        self.outline_line_join = outline_line_join
        
        super(TextUniform, self).__init__(x, y, w, h, text, halign, valign, yoffset, margin)
        
    def _draw(self, surface, x, y, w, h):
        
        cr = cairo.Context(surface)
        
        pc_layout = self._get_pc_layout(cr, w, h)
        
        profile('text.draw')
        if(self.stroke_src is not None):
            cr.move_to(x, y)
            cr.set_line_width(self.stroke_width * 2)
            self.stroke_src.set(cr, 0, 0, w, h)
            cr.set_line_join(self.outline_line_join)
            pc.update_layout(cr, pc_layout)
            pc.layout_path(cr, pc_layout)
            cr.stroke()
        
        cr.save()
        cr.move_to(x, y)
        self.fill_src.set(cr, 0, 0, w, h)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        pc.update_layout(cr, pc_layout)
        pc.layout_path(cr, pc_layout)
        cr.fill()
        cr.restore()
        profile()
        
    def _get_pc_layout(self, cr, w, h):
        pc_layout = pc.create_layout(cr)
        if w is not None:
            pc_layout.set_width(int(w) * PANGO_SCALE)
        desc = self.font_description.get_pango_font_description()
        pc_layout.set_font_description(desc)
        pc_layout.set_text(self.text)
        pc_layout.set_spacing(self.spacing)
        pc_layout.set_alignment(convert_to_pango_align(self.halign))
        
        return pc_layout
        
    def _get_text_size(self, w, h):
        cr = cairo.Context(TextUniform.dummy_surface)
        pc_layout = self._get_pc_layout(cr, w, h)

        ink, logical = pc_layout.get_extents()
        pc_layout.get_iter()
        
        return ink.x / PANGO_SCALE - self.stroke_width, logical.y / PANGO_SCALE - self.stroke_width, \
               ink.width / PANGO_SCALE + 2 * self.stroke_width, \
               logical.height / PANGO_SCALE + 2 * self.stroke_width
    
if __name__ == '__main__':
    
    bg = Rectangle(0, 0, 400, 400, layout=VerticalFlowLayout(HALIGN_CENTER))
    
    text = TextUniform(
        10, 10, '100%', '100%', "testing text", font_description=FontDescription(size=40),
        halign=HALIGN_CENTER, valign=VALIGN_MIDDLE, stroke_width=5, stroke_src=(1, 0, 0, 1), fill_src=(0, 1, 0, 1),
        outline_line_join=cairo.LINE_JOIN_ROUND
    )
    
    markup = '&gt;&lt;&amp;<span font_desc="Arial Italic 20">testing text</span> and\n' +\
             '<span font_desc="Sans Bold 25" foreground="#ff3456">testing &amp;text 2&amp;</span>'

    replace_glyph = Rectangle(0, 1, 15, 25, 5, stroke_color=(0.7, 0.5, 0.3, 1),
                                     fill_color=(0.9, 0.4, 0.9, 0.75))

    # text = TextMarkup(
    #     10, 10, '100%', '100%', markup, halign=HALIGN_CENTER, valign=VALIGN_MIDDLE, text_replace_map={'&': replace_glyph})

    text = TextMarkup(
        10, 10, '100%', '100%', '<span foreground="#ff0000">this is\na longer text</span>', halign=HALIGN_RIGHT, valign=VALIGN_BOTTOM)
    
    bg.add(text)
    bg.image().show()
    bg.image().save('output/testing text3 .png')
    
    profile.results()