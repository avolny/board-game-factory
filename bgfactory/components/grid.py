from collections.abc import Iterable
from math import floor, ceil
from warnings import warn

import cairocffi as cairo

from bgfactory.common.profiler import profile
from bgfactory.components.cairo_helpers import adjust_rect_size_by_line_width
from bgfactory.components.component import Component
from bgfactory.components.constants import FILL, INFER, COLOR_TRANSPARENT, COLOR_BLACK, \
    COLOR_WHITE, HALIGN_CENTER, VALIGN_MIDDLE
from bgfactory.components.layout.layout_manager import LayoutError
from bgfactory.components.layout.vertical_flow_layout import VerticalFlowLayout
from bgfactory.components.shape import Rectangle
from bgfactory.components.source import convert_source
from bgfactory.components.text import TextUniform
from bgfactory.components.utils import is_percent, parse_percent


def _default_kwargs_generator(i, j):
    return dict()


class GridError(ValueError):
    pass


class Grid(Component):

    def __init__(
            self, x, y, w, h, cols, rows, hspace=0, vspace=0, cell_kwargs_generator=None, stroke_width=0,
            stroke_src=COLOR_BLACK, fill_src=COLOR_TRANSPARENT, margin=(0, 0, 0, 0), padding=(0, 0, 0, 0)):
        """
        Initialize Grid component. It allows for very complex layouts, it is akin to LayoutManager but there
        are good reasons why it's a Component.
        :param x: x coordinate of the Grid 
        :param y: y coordinate of the Grid 
        :param w: width of the Grid, values: px, '{value}%', INFER, FILL 
        :param h: height of the Grid, values: px, '{value}%', INFER, FILL
        :param cols: int for number of uniform columns, or list of column widths, possible values: px, '{value}%', INFER, FILL
        :param rows: int for number of uniform rows, list of row heights, possible values: px, '{value}%', INFER, FILL
        :param hspace: sets horizontal spaces between columns, either float or a list of spacings, when using
        the list, the following must hold: len(hspace) = len(cols) - 1
        :param vspace: sets vertical spaces between rows, either float or a list of spacings, when using
        the list, the following must hold: len(vspace) = len(rows) - 1
        :param cell_kwargs_generator: a function(i, j) -> dict() that allows to pass custom parameters to each
        separate cell when calling its constructor. following kwargs can be set:
            stroke_width, stroke_color, fill_color, padding, layout
        when either stroke_width, stroke_color or fill_color are not set, the values for grid are used
        :param stroke_width: width of the grid separators, note that the visual width will always be double,
        since each cell draws its own border. If you need a border of exactly 1 px, set stroke_width=0,
        using cell_kwargs_generator set stroke_width=1 for all the cells and then set hspace=-1, vspace=-1. This
        will result in 1-pixel border grid. You can use the same procedure to generate any odd-pixel border
        :param stroke_src: source of the border (color tuple or Source)
        :param fill_src: fill color of the grid
        :param margin: margin (4-tuple - left, top, right, bot)
        :param padding: padding (4-tuple - left, top, right, bot)
        """

        self.stroke_width = stroke_width
        self.stroke_src = convert_source(stroke_src)
        self.fill_src = convert_source(fill_src)
        self.padding = [e + stroke_width for e in padding]

        if isinstance(rows, int):
            rows = [f'{100 / rows:.02f}%'] * rows
        if isinstance(cols, int):
            cols = [f'{100 / cols:.02f}%'] * cols

        self.rows = rows
        self.cols = cols

        nrows = len(self.rows)
        ncols = len(self.cols)

        try:
            ix = self.rows.index(FILL)
            if ix != nrows - 1:
                raise ValueError('FILL can be set only in the last column and the last row')
        except ValueError:
            pass

        try:
            ix = self.cols.index(FILL)
            if ix != ncols - 1:
                raise ValueError('FILL can be set only in the last column and the last row')
        except ValueError:
            pass
        
        if w == INFER:
            for col in self.cols:
                if col == FILL:
                    raise ValueError('There can\'t be a column with width="fill" when w=="infer"')
                if is_percent(col):
                    raise ValueError('There can\'t be a column with width=n% when w=="infer"')
        elif isinstance(w, float):
            w = round(w)

        if h == INFER:
            for row in self.rows:
                if row == FILL:
                    raise ValueError('There can\'t be a column with height="fill" when h=="infer"')
                if is_percent(row):
                    raise ValueError('There can\'t be a column with height=n% when h=="infer"')
        elif isinstance(h, float):
            h = round(h)

        if vspace is None:
            vspace = 0
        if isinstance(vspace, (int, float)):
            self.vspace = [round(vspace)] * (nrows - 1)
        elif isinstance(vspace, Iterable):
            self.vspace = list(vspace)
            if len(self.vspace) != nrows - 1:
                raise ValueError('If vspace is iterable, it must hold: len(vspace) == len(rows) - 1')

        if hspace is None:
            hspace = 0
        if isinstance(hspace, (int, float)):
            self.hspace = [hspace] * (ncols - 1)
        elif isinstance(hspace, Iterable):
            self.hspace = list(hspace)
            if len(self.hspace) != ncols - 1:
                raise ValueError('If hspace is iterable, it must hold: len(hspace) == len(cols) - 1')

        if cell_kwargs_generator is None:
            cell_kwargs_generator = _default_kwargs_generator
        
        self.cells = []
        for i in range(nrows):
            self.cells.append([])
            for j in range(ncols):
                kwargs = dict(
                    stroke_width=stroke_width,
                    stroke_src=stroke_src,
                    fill_src=fill_src,
                    padding=(0, 0, 0, 0),
                    layout=None)
                kwargs.update(cell_kwargs_generator(i, j))
                
                self.cells[i].append(GridCell(cols[j], rows[i], 1, 1, **kwargs))
                
        super(Grid, self).__init__(x, y, w, h, margin)

    def cell_merge_right(self, i, j):
        """
        Merge into the cell (i,j) all cells to its right. All merged cells
        are always represented by the leftmost uppermost cell, so calling this
        repeatedly on the same cell will merge more and more cells.
        
        :param i: row of the master cell
        :param j: column of the master cell
        :return:
        """
        
        cell = self.cells[i][j]
        
        if cell is None:
            raise ValueError('trying to merge an empty cell')
        
        if j < 0 or j >= len(self.cols) - 1 - cell._gridw + 1:
            raise IndexError('The column index ({}) is out of range for ncols={} and master cell width={}'.format(
                j, len(self.cols), cell._gridw))
        
        j += cell._gridw - 1
        
        for k in range(cell._gridh):
            cell_to_merge = self.cells[i + k][j + 1]
            if len(cell_to_merge.children) > 0:
                warn('You are merging a cell ({}, {}) with nonempty children. '
                     'All children of the merged cell are removed. '
                     'In general, it\' recommended to setup layout before adding content.'.format(i + k, j + 1))

        cell._gridw += 1
        for k in range(cell._gridh):
            self.cells[i + k][j + 1] = None

    def cell_merge_down(self, i, j):
        """
        Merge into the cell (i,j) all cells to its right. All merged cells
        are always represented by the leftmost uppermost cell, so calling this
        repeatedly on the same cell will merge more and more cells.

        :param i: row of the master cell
        :param j: column of the master cell
        :return:
        """

        cell = self.cells[i][j]
        
        if cell is None:
            raise ValueError('trying to merge an empty cell')

        if i < 0 or i >= len(self.rows) - 1 - cell._gridh + 1:
            raise IndexError('The column index ({}) is out of range for ncols={} and master cell width={}'.format(
                i, len(self.rows), cell._gridh))

        i += cell._gridh - 1

        for k in range(cell._gridw):
            cell_to_merge = self.cells[i + 1][j + k]
            if len(cell_to_merge.children) > 0:
                warn('You are merging a cell ({}, {}) with nonempty children. '
                     'All children of the merged cell are removed. '
                     'In general, it\' recommended to setup layout before adding content.'.format(i + 1, j + k))

        cell._gridh += 1
        for k in range(cell._gridw):
            self.cells[i + 1][j + k] = None
    
    def add(self, i, j, child):
        self.cells[i][j].add(child)
        
    def __getitem__(self, item):
        if isinstance(item, (list, tuple)) and len(item) in [1, 2]:
            if len(item) == 2:
                return self.cells[item[0]][item[1]]
            else:
                return self.cells[item]
        else:
            raise ValueError('Only single integer or 2-tuple indexing is allowed like grid[3] or grid[1, 2]')

    def _draw_outline(self, surface: cairo.Surface, w, h):
        cr = cairo.Context(surface)

        x, y, w, h = adjust_rect_size_by_line_width(0, 0, w, h, self.stroke_width)
        cr.rectangle(x, y, w, h)

        cr.set_line_width(self.stroke_width)
        self.fill_src.set(cr, 0, 0, w, h)
        cr.fill_preserve()
        self.stroke_src.set(cr, 0, 0, w, h)
        cr.stroke()
        
    def _get_cell_area_width(self, w):
        """
        Returns width to be filled by cells
        :param w: 
        :return: 
        """
        if self.cols[-1] == FILL:
            return w
        else:
            total_percent = 0
            total_pixels = 0
            
            for j, col_def in enumerate(self.cols):
                if col_def == INFER:
                    total_pixels += self._infer_col_width(j)
                elif is_percent(col_def):
                    total_percent += parse_percent(col_def)
                else:
                    total_pixels += col_def
                    
            w_remainder = w - total_pixels
            
            w_percent = ceil(total_percent * w_remainder)
            
            return max(0, min(total_pixels + w_percent, w))
            
    def _get_cell_area_height(self, h):
        """
        Returns height to be filled by cells
        :param h: 
        :return: 
        """
        if self.rows[-1] == FILL:
            return h
        else:
            total_percent = 0
            total_pixels = 0

            for j, row_def in enumerate(self.rows):
                if row_def == INFER:
                    total_pixels += self._infer_row_height(j)
                elif is_percent(row_def):
                    total_percent += parse_percent(row_def)
                else:
                    total_pixels += row_def

            h_remainder = h - total_pixels

            h_percent = ceil(total_percent * h_remainder)

            return max(0, min(total_pixels + h_percent, h))
    
    def _infer_col_width(self, col_id):
        nrows = len(self.rows)
        
        w_max = 0
        for i in range(nrows):
            cell = self.cells[i][col_id]
            if cell is not None and cell._can_infer and cell._gridw == 1: # do not use merged cells for inferring width
                w_max = max(w_max, cell.get_size()[0])
                
        return w_max
    
    def _infer_row_height(self, row_id):
        ncols = len(self.cols)
        
        h_max = 0
        for j in range(ncols):
            cell = self.cells[row_id][j]
            if cell is not None and cell._can_infer and cell._gridh == 1:
                h_max = max(h_max, cell.get_size()[1])
                
        return h_max
    
    def _get_col_widths(self, w):
        # w is in pixels or None
        
        widths = []
        
        ncols = len(self.cols)
        nrows = len(self.rows)
        
        if w is None:
            w = 0
        
        w_available = self._get_cell_area_width(w - self.padding[0] - self.padding[2] - sum(self.hspace))
        w_remainder = w_available
        
        for j in range(ncols):
            
            col_width = self.cols[j]
            
            if col_width == INFER:
                cw = self._infer_col_width(j)
            elif is_percent(col_width):
                cw = floor(parse_percent(col_width) * w_available)
            elif col_width == FILL:
                cw = w_remainder
            elif isinstance(col_width, (float, int)):
                cw = col_width
            else:
                raise ValueError('unrecognized width value: {}'.format(col_width))
            
            widths.append(cw)
            w_remainder -= cw
            
        while w_remainder > 0:
            for i in range(len(widths)):
                delta = min(1, w_remainder)
                w_remainder -= delta
                widths[i] += delta
                
                if w_remainder <= 0:
                    break
            
        if w_remainder < 0 and w > 0:
            warn('The grid contents are wider than the grid component itself.')
            
        return widths
    
    def _get_row_heights(self, h):
        heights = []

        ncols = len(self.cols)
        nrows = len(self.rows)

        if h is None:
            h = 0

        h_available = self._get_cell_area_height(h - round(self.padding[1]) - round(self.padding[3]) - sum(self.vspace))
        h_remainder = h_available
        
        for i in range(nrows):

            row_height = self.rows[i]

            if row_height == INFER:
                ch = self._infer_row_height(i)
            elif is_percent(row_height):
                ch = floor(parse_percent(row_height) * h_available)
            elif row_height == FILL:
                ch = h_remainder
            elif isinstance(row_height, (float, int)):
                ch = row_height
            else:
                raise ValueError('unrecognized height value: {}'.format(row_height))

            heights.append(ch)
            h_remainder -= ch

        while h_remainder > 0:
            for i in range(len(heights)):
                delta = min(1, h_remainder)
                h_remainder -= delta
                heights[i] += delta

                if h_remainder <= 0:
                    break

        if h_remainder < 0 and h > 0:
            warn('The grid contents are taller than the grid component itself.')

        return heights
    
    def draw(self, w, h):
        
        surface = super(Grid, self).draw(w, h)
        self._draw_outline(surface, w, h)

        cr = cairo.Context(surface)
        
        ncols = len(self.cols)
        nrows = len(self.rows)
        
        widths = self._get_col_widths(w)
        heights = self._get_row_heights(h)
        
        cy = self.padding[1]
        
        for i in range(nrows):

            cx = self.padding[0]
            for j in range(ncols):

                cell = self.cells[i][j]
                
                if cell is not None:

                    cw = 0
                    ch = 0
                    
                    # compute width and height based on gridw and gridh (those allow merged cells)
                    for k in range(cell._gridw):
                        cw += widths[j + k]
                        if k < cell._gridw - 1:
                            cw += self.hspace[j + k]
                            
                    for k in range(cell._gridh):
                        ch += heights[i + k]
                        if k < cell._gridh - 1:
                            ch += self.vspace[i + k]
                            
                    child_surface = cell.draw(cw, ch)
                    profile('paint child surface')
                    cr.set_source_surface(child_surface, cx, cy)
                    cr.paint()
                    profile()
                else:
                    pass

                cx += widths[j]
                if j < ncols - 1:
                    cx += self.hspace[j]

            cy += heights[i]
            if i < nrows - 1:
                cy += self.vspace[i]
                
        return surface
                
    def get_size(self):
        if self.w != INFER:
            w = self.w
        else:
            widths = self._get_col_widths(None)
            w = sum(widths) + sum(self.hspace) + self.padding[0] + self.padding[2]

        if self.h != INFER:
            h = self.h
        else:
            heights = self._get_row_heights(None)
            h = sum(heights) + sum(self.vspace) + self.padding[1] + self.padding[3]

        return w, h


class GridCell(Rectangle):

    def __init__(self, w, h, gridw, gridh, layout, stroke_width, stroke_src, fill_src, padding):
        self._gridw = gridw
        self._gridh = gridh
        self._can_infer = True

        super(GridCell, self).__init__(
            0, 0, w, h, layout=layout, stroke_width=stroke_width, stroke_src=stroke_src, fill_src=fill_src, padding=padding)
        
    def add(self, child):
        
        try:
            self.layout.validate_child(child)
        except LayoutError:
            self._can_infer = False
            
        self.children.append(child)

if __name__ == '__main__':
    
    rect = Rectangle(0, 0, 500, 500, stroke_width=0, fill_src=COLOR_WHITE)
    
    grid = Grid(30, 30, 400, 400,
        ['5%', '30%', '10%', FILL],
        [50, 100, 20, FILL], -1, -1, stroke_width=0, cell_kwargs_generator=lambda i,j: dict(
            layout=VerticalFlowLayout(HALIGN_CENTER, VALIGN_MIDDLE),
            stroke_width=1
        )
    )
    
    grid.cells[0][3].add(TextUniform(0, 0, INFER, INFER, 'This is a text'))
    grid.cells[3][1].add(TextUniform(0, 0, INFER, INFER, 'This is a text too'))

    # grid.cell_merge_right(1, 1)
    grid.cell_merge_right(1, 2)
    grid.cell_merge_down(1, 2)
    
    # grid.cell_merge_right(1, 1)
    # grid.cell_merge_right(1, 1)
    # grid.cell_merge_right(0, 0)
    # grid.cell_merge_right(0, 0)
    # grid.cell_merge_right(0, 0)
    # grid.cell_merge_right(2, 0)
    # grid.cell_merge_right(2, 0)
    # grid.cell_merge_right(2, 0)
    # grid.cell_merge_right(3, 0)
    # grid.cell_merge_right(3, 0)
    # grid.cell_merge_right(3, 0)
    
    # grid.image().show()
    rect.add(grid)
    
    # rect.image().save('output/test grid.png')
    rect.image().show()

    
