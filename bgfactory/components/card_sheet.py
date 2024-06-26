from os import makedirs
from pathlib import Path

from bgfactory.components.constants import COLOR_WHITE, INFER, COLOR_BLACK
from bgfactory.components.shape import Rectangle, Line
from bgfactory.components.text import TextUniform, FontDescription
from bgfactory.components.utils import A4_WIDTH_MM, A4_HEIGHT_MM, mm_to_pixels


class CardSheet(Rectangle):
    
    def __init__(self, w, h, cards, reversed=False, cutlines=True, page=None,
                 overspill_border_width=0, overspill_border_color=COLOR_BLACK):

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

        overspill_rect = Rectangle(padx - overspill_border_width, pady - overspill_border_width, w - 2 * padx + 2 * overspill_border_width, h - 2 * pady + 2 * overspill_border_width,
                                   stroke_src=overspill_border_color,
                                   stroke_width=overspill_border_width * 2)

        self.add(overspill_rect)
        
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
            pad_outside = 5
            pad_inside = 15
            for i in range(self.nrows + 1):
                self.add(Line(pad_outside, pady + ch * i, padx - pad_inside, pady + ch * i, 
                              stroke_width=2, dash={'dashes': [10, 5]}))
                self.add(Line(w - padx + pad_inside, pady + ch * i, w - pad_outside, pady + ch * i,
                              stroke_width=2, dash={'dashes': [10, 5]}))
                
            for i in range(self.ncols + 1):
                self.add(Line(padx + cw * i, pad_outside, padx + cw * i, pady - pad_inside, 
                              stroke_width=2, dash={'dashes': [10, 5]}))
                self.add(Line(padx + cw * i, h - pady + pad_inside, padx + cw * i, h - pad_outside,
                              stroke_width=2, dash={'dashes': [10, 5]}))
        
    def get_size(self):
        return self.w, self.h


def make_printable_sheets(
        components, dpi=300, print_margin_hor_mm=5, print_margin_ver_mm=5, page_width_mm=None, page_height_mm=None,
        overspill_border_mm=1, overspill_border_src=COLOR_BLACK,
        orientation='auto', cutlines=True, page_numbers=True, out_dir_path=None, out_file_prefix='sheet', out_dir_jpeg_path=None):
    if page_width_mm is None or page_height_mm is None:
        page_width_mm = A4_WIDTH_MM
        page_height_mm = A4_HEIGHT_MM

    w = mm_to_pixels(page_width_mm - 2 * print_margin_hor_mm, dpi)
    h = mm_to_pixels(page_height_mm - 2 * print_margin_ver_mm, dpi)

    if orientation == 'auto':
        sheet = CardSheet(w, h, components)
        n_portrait = sheet.nrows * sheet.ncols

        sheet = CardSheet(h, w, components)
        n_landscape = sheet.nrows * sheet.ncols

        if n_portrait >= n_landscape:
            orientation = 'portrait'
        else:
            orientation = 'landscape'

    if orientation == 'portrait':
        w, h = w, h
    elif orientation == 'landscape':
        w, h = h, w
    else:
        raise ValueError(f'unknown {orientation=}, allowed values: auto, portrait, landscape')

    sheet = CardSheet(w, h, components)
    components_per_page = sheet.nrows * sheet.ncols

    sheets = []

    page = 1
    for i in range(0, len(components), components_per_page):
        sheet = CardSheet(
            w, h, components[i:i + components_per_page],
            cutlines=cutlines,
            page=page if page_numbers else None,
            overspill_border_width=mm_to_pixels(overspill_border_mm, dpi),
            overspill_border_color=overspill_border_src
        )
        page += 1

        sheets.append(sheet)

    if out_dir_path is not None:
        out_dir_path = Path(out_dir_path)

        makedirs(out_dir_path, exist_ok=True)

        for index, sheet in enumerate(sheets):
            sheet.image().save(out_dir_path / f'{out_file_prefix}{index:02d}.png')

    if out_dir_jpeg_path is not None:
        out_dir_jpeg_path = Path(out_dir_jpeg_path)

        makedirs(out_dir_jpeg_path, exist_ok=True)

        for index, sheet in enumerate(sheets):
            sheet.image().convert('RGB').save(out_dir_jpeg_path / f'{out_file_prefix}{index:02d}.jpg', 'JPEG', quality=90, optimize=True)

    return sheets
