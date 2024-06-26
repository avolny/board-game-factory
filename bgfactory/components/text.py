from abc import abstractmethod
from math import ceil
from typing import Mapping
from warnings import warn

from xml.etree import ElementTree

import cairocffi as cairo
import pangocffi as pango
import pangocairocffi as pc

from bgfactory.common.config import bgfconfig
from bgfactory.components.component import Component, DEBUG
from bgfactory.components.constants import COLOR_BLACK, INFER, HALIGN_LEFT, VALIGN_TOP, \
    HALIGN_CENTER, HALIGN_RIGHT, VALIGN_MIDDLE, VALIGN_BOTTOM, FILL
from bgfactory.components.layout.vertical_flow_layout import VerticalFlowLayout
from bgfactory.components.shape import Rectangle
from bgfactory.components.pango_helpers import PANGO_SCALE, convert_to_pango_align, convert_extents
from bgfactory.common.profiler import profile
from bgfactory.components.source import convert_source
from bgfactory.components.utils import is_percent, parse_percent


SHOW_ME_DIMENSIONS = 'show_me_dimensions'


class FontDescription():

    def __init__(
            self,
            family="Arial",
            size=12,
            weight=pango.Weight.NORMAL,
            style=pango.Style.NORMAL,
            stretch=pango.Stretch.NORMAL,
            gravity=pango.Gravity.AUTO):
        
        self.family = family
        self.size = size

        font_desc = pango.FontDescription()

        font_desc.family = family
        font_desc.set_absolute_size(size * PANGO_SCALE)
        font_desc.weight = weight
        font_desc.style = style
        font_desc.stretch = stretch
        font_desc.gravity = gravity

        self._desc = font_desc
    
    def get_pango_font_description(self):
        return self._desc


class _TextComponent(Component):

    def __init__(self, x, y, w, h, text, halign, valign, yoffset, margin):
        
        if not isinstance(text, str):
            # warn(f'text={text} is not string, converting by str()')
            text = str(text)
        
        self.text = text
        self.yoffset = yoffset
        self.halign = halign
        self.valign = valign
        
        if w == FILL:
            raise ValueError('Width on a text component cannot be set to fill.'
                             'This is because of the function get_size() it has'
                             'no way to find out the available space')
        
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
            fh = h
            
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
        
        # print(self.text)
        # print(self._get_text_size(w, h))
        
        if htext > h:
            warn('The text contents are higher than the display area, expect some text to be cut off. '
                 'In general to avoid this, avoid using FILL or "n%" on width while using INFER on height of this element. '
                 'When computing the height, the FILL or percentage width is not taken into account and any extra text '
                 'will get cutoff')

        htext += self.yoffset

        # x = -xoffset
        # y = self.yoffset - yoffset
        
        # print(w, h)

        if (self.halign == HALIGN_CENTER):
            x = w / 2 - (wtext) / 2 - xoffset
        elif (self.halign == HALIGN_RIGHT):
            x = w - wtext - xoffset
        else:
            x = -xoffset
        # else:
        #     x -= xoffset

        if (self.valign == VALIGN_MIDDLE):
            y = h / 2 - htext / 2 + self.yoffset - yoffset
        elif (self.valign == VALIGN_BOTTOM):
            y = h - htext + self.yoffset - yoffset
        else:
            y = self.yoffset - yoffset
        # else:
        #     y += self.yoffset - yoffset
            
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

    def __init__(self, x, y, w, h, text, font_description=FontDescription(), spacing=0.115, halign=HALIGN_LEFT,
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
         To figure out the dimensions of the removed text, use 'your_key': SHOW_ME_DIMENSIONS entries and the draw
         method will produce both console output with the dimensions and visual guides. Note that the glyphs are not
         constrained by these dimensions but those are used as reference for FILL and n% of the glyphs. 

        :param margin: 
        """
        
        self.spacing = spacing
        if text_replace_map is None:
            text_replace_map = dict()
        self.text_replace_map = text_replace_map
        self.font_desc = font_description
        
        super(TextMarkup, self).__init__(x, y, w, h, text, halign, valign, yoffset, margin)
        
    def _draw(self, surface, x, y, w, h):
        cr = cairo.Context(surface)

        pc_layout = self._get_pc_layout(cr, w, h)

        profile('text.draw')
        
        # print('draw ', x, y, w, h)

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
        
        replacements = [None] * len(text)
        replacement_keys = [None] * len(text)
        replacement_lengths = [0] * len(text)
        
        CONTINUE = 'continue'
        END = 'end'
        
        for key in self.text_replace_map:
            split = text.split(key)
            
            index = len(split[0])
            
            for part in split[1:]:
                replacements[index] = self.text_replace_map[key]
                replacement_keys[index] = key
                replacement_lengths[index] = len(key)
                index += len(part) + len(key)
        
        if not text:
            return
        
        char_index = 0
        
        replacement_width = None
        replacement_height = None
        replacement_finish = None
        replacement_x = None
        replacement_y = None
        
        while True:
            
            # char = text[char_index]
            ext = layout_iter.get_char_extents()
            y_baseline = base_y + layout_iter.get_baseline() / PANGO_SCALE
            x, y, w, h = base_x + ext.x / PANGO_SCALE, base_y + ext.y / PANGO_SCALE, ext.width / PANGO_SCALE, ext.height / PANGO_SCALE
            ink, log = layout_iter.get_cluster_extents()

            # print(text[char_index], convert_extents(ext))
            # print(text[char_index], convert_extents(ink), convert_extents(log))
            
            # print(convert_extents(ext2))
            
            if replacements[char_index]:
                # print(layout_iter.get_index())
                # print(x, y, w, h)
                
                replacement_glyph = replacements[char_index]
                replacement_key = replacement_keys[char_index]
                replacement_finish = char_index + replacement_lengths[char_index] - 1
                
                # print(replacement_glyph)
                # print(replacement_finish)
                
                replacement_x = x
                replacement_y = y
                replacement_width = w
                replacement_height = h
            elif replacement_finish is not None:
                replacement_width += w
                replacement_height = max(replacement_height, h)
            
            if char_index == replacement_finish:
                
                cr.save()
                # clear out the glyph area
                cr.move_to(replacement_x, replacement_y)
                cr.rectangle(replacement_x, replacement_y, replacement_width, replacement_height)
                cr.set_operator(cairo.OPERATOR_CLEAR)
                cr.set_tolerance(bgfconfig.tolerance)
                cr.fill()
                cr.restore()
                
                # it makes more sense to adjust the height to the baseline
                replacement_height = y_baseline - replacement_y
                
                if replacement_glyph == SHOW_ME_DIMENSIONS:
                    print('show me dimensions for: {}'.format(replacement_key))
                    print('removed glyphs: x {}, y {}, w {}, h {}, y_baseline {}'.format(
                        replacement_x, replacement_y, replacement_width, replacement_height, y_baseline))
                    replacement_glyph = Rectangle(0, 0, FILL, FILL, stroke_width=3, stroke_src=(0.8, 0.3, 0.1, 0.5),
                                                   fill_src=(0.3, 0.5, 0.5, 0.5))
                
                w, h = replacement_glyph.get_size()
                if w == FILL:
                    w = '100%'
                if is_percent(w):
                    w = replacement_width * parse_percent(w)
                if h == FILL:
                    h = '100%'
                if is_percent(h):
                    h = replacement_height * parse_percent(h)
                
                # print(replacement_width, replacement_height, w, h)
                
                surface = replacement_glyph.draw(w, h)
                
                # place the glyph on the line baseline to the middle of the removed glyph,
                # the glyph x,y coordinates are used as an offset
                x_glyph = replacement_x + replacement_width / 2 - w / 2 + replacement_glyph.x
                
                y_glyph = y_baseline - h + replacement_glyph.y
                
                # print(y_baseline)
                # print(h)
                # print(y_glyph)

                cr.set_source_surface(surface, x_glyph, y_glyph)
                cr.set_tolerance(bgfconfig.tolerance)
                cr.paint()
                
                replacement_glyph = None
                replacement_finish = None
            
            char_index += 1
            
            if not layout_iter.next_char():
                break

    # def _get_pc_layout(self, cr, w, h):
    #     pc_layout = pc.create_layout(cr)
    #     if w is not None:
    #         pc_layout._set_width(int(w * PANGO_SCALE))
    #     pc_layout._set_font_description(self.font_desc._desc)
    #     pc_layout._set_text(self.text)
    #     pc_layout.set_markup(self.text)
    #     pc_layout._set_spacing(int(self.spacing * self.font_desc.size * PANGO_SCALE))
    #     pc_layout._set_alignment(convert_to_pango_align(self.halign))
    #
    #     return pc_layout

    def _get_pc_layout(self, cr, w, h):
        pc_layout = pc.create_layout(cr)
        if w is not None:
            pc_layout.width = int(w) * PANGO_SCALE
        pc_layout.font_description = self.font_desc._desc
        pc_layout.apply_markup(self.text)
        pc_layout.spacing = int(self.spacing * self.font_desc.size * PANGO_SCALE)
        pc_layout.alignment = convert_to_pango_align(self.halign)

        return pc_layout

    def _get_text_size(self, w, h):
        cr = cairo.Context(TextUniform.dummy_surface)
        pc_layout = self._get_pc_layout(cr, w, h)

        ink, logical = pc_layout.get_extents()

        # print(ink.x / PANGO_SCALE, ink.y / PANGO_SCALE, ink.width / PANGO_SCALE, ink.height / PANGO_SCALE)
        # print(logical.x / PANGO_SCALE, logical.y / PANGO_SCALE, logical.width / PANGO_SCALE, logical.height / PANGO_SCALE)

        return logical.x / PANGO_SCALE, logical.y / PANGO_SCALE, logical.width / PANGO_SCALE, logical.height / PANGO_SCALE

    def _xml_to_plaintext(self, text):
        return ''.join(ElementTree.fromstring('<root>' + text + '</root>').itertext())
    
    
class TextUniform(_TextComponent):
    """
    A basic Text component that assumes uniform text style. Allows for text outline,
    for making pretty titles etc.
    """
    dummy_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)
    
    def __init__(self, x, y, w, h, text, font_description=FontDescription(), spacing=0.115, halign=HALIGN_LEFT,
                 valign=VALIGN_TOP, fill_src=COLOR_BLACK, stroke_width=0, stroke_src=None,
                 outline_line_join=cairo.LINE_JOIN_MITER, yoffset=0, margin=(0,0,0,0)):
        
        self.font_description = font_description
        self.fill_src = convert_source(fill_src)
        self.stroke_width = stroke_width
        self.stroke_src = convert_source(stroke_src)
        self.spacing = spacing
        self.outline_line_join = outline_line_join
        
        super(TextUniform, self).__init__(round(x), round(y), w, h, text, halign, valign, yoffset, margin)
        
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
            cr.close_path()
            cr.stroke()

        cr.save()
        cr.move_to(x, y)
        self.fill_src.set(cr, 0, 0, w, h)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        pc.update_layout(cr, pc_layout)
        pc.layout_path(cr, pc_layout)
        cr.set_tolerance(bgfconfig.tolerance)
        cr.close_path()
        cr.fill()
        cr.restore()
        profile()
        
    def _get_pc_layout(self, cr, w, h):
        pc_layout = pc.create_layout(cr)
        if w is not None:
            pc_layout.width = int(w) * PANGO_SCALE
        pc_layout.font_description = self.font_description._desc
        pc_layout.text = self.text
        pc_layout.spacing = int(self.spacing * self.font_description.size * PANGO_SCALE)
        pc_layout.alignment = convert_to_pango_align(self.halign)
        
        return pc_layout
        
    def _get_text_size(self, w, h):
        cr = cairo.Context(TextUniform.dummy_surface)
        pc_layout = self._get_pc_layout(cr, w, h)

        ink, logical = pc_layout.get_extents()
        # pc_layout.get_iter()
        
        return logical.x / PANGO_SCALE - self.stroke_width, logical.y / PANGO_SCALE - self.stroke_width, \
               logical.width / PANGO_SCALE * 1.021 + 2 * self.stroke_width, \
               logical.height / PANGO_SCALE + 2 * self.stroke_width
    
if __name__ == '__main__':
    bg = Rectangle(0, 0, 400, 400, layout=VerticalFlowLayout(HALIGN_CENTER))

    text = TextUniform(
        10, 10, '100%', '100%', "testing\ntext", font_description=FontDescription(
            size=24, family='Arial', style=pango.Style.OBLIQUE, weight=pango.Weight.BOLD),
        halign=HALIGN_CENTER, valign=VALIGN_MIDDLE, stroke_width=5, stroke_src=(1, 0, 0, 1), fill_src=(0, 1, 0, 1),
        outline_line_join=cairo.LINE_JOIN_ROUND
    )

    markup = '&gt;&lt;&amp;<span font_desc="Arial Italic 20">testing text</span> and\n' +\
             '<span font_desc="Sans Bold 25" foreground="#ff3456">testing &amp;text 2&amp;</span>'

    replace_glyph = Rectangle(0, 1, 15, 25, 5, stroke_src=(0.7, 0.5, 0.3, 1),
                                     fill_src=(0.9, 0.4, 0.9, 0.75))

    text = TextMarkup(
        10, 10, '100%', '100%', markup, halign=HALIGN_CENTER, valign=VALIGN_MIDDLE, text_replace_map={'&': replace_glyph})

    # text = TextMarkup(10, 10, '100%', '100%', '<span foreground="#ff0000">this is\na longer text</span>',
    #                   halign=HALIGN_RIGHT, valign=VALIGN_BOTTOM)

    bg.add(text)
    bg.image().show()
    # bg.image().save('output/testing text3 .png')
    
    # profile.results()