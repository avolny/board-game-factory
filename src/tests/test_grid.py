from bgfactory.components.constants import INFER, HALIGN_CENTER, VALIGN_MIDDLE, \
    FILL
from bgfactory.components.grid import Grid
from bgfactory.components.layout.vertical_flow_layout import VerticalFlowLayout
from bgfactory.components.shape import Rectangle
from tests.utils import ComponentRegressionTestCase


class TestGrid(ComponentRegressionTestCase):
    MERGE_RIGHT = [
        [],
        [(1, 1), (1, 1)],
    ]
    
    MERGE_BOT = [
        [],
        [(1, 1), (3, 3)],
    ]
    
    COLS = [
        [80],
        ['40%'],
        [FILL],
        [INFER],
        [45, '30%', 45, INFER, FILL],
        [INFER, '10%', '10%', '15%', FILL],
        [INFER, INFER, INFER, INFER, INFER]
    ]
    
    ROWS = [
        [50],
        ['30%'],
        [FILL],
        [INFER],
        [INFER, 50, '25%', INFER, FILL],
        ['30%', '30%', INFER, '20%', FILL],
        [INFER, INFER, INFER, INFER, INFER]
    ]
    
    HSPACE = [
        0,
        5,
        [4, 5, 6, 7]
    ]
    
    VSPACE = [
        0,
        5,
        [6, 7, 8, 9]
    ]
    
    PADDING = [
        (0, 0, 0, 0),
        (5, 5, 5, 5),
        (5, 6, 7, 8)
    ]
    
    @staticmethod
    def kwargs1(i, j):
        return dict(layout=VerticalFlowLayout(HALIGN_CENTER, VALIGN_MIDDLE))

    @staticmethod
    def kwargs2(i, j):
        return dict(
            stroke_width=i,
            stroke_src=(i * 0.1, j * 0.1, 0.5, 1),
            fill_src=(0.5, j * 0.1, i * 0.1, 0.7),
            padding=(i, j, i, j),
            layout=VerticalFlowLayout(HALIGN_CENTER, VALIGN_MIDDLE)
        )
    

    @staticmethod
    def generate_test_variants():
        args = [
            [400, 400, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [400, 400, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [400, 400, 2, 2, 0, 0, 1, 0, 0, 0, 0],
            [400, 400, 3, 3, 0, 0, 1, 0, 0, 0, 0],
            [INFER, 400, 3, 2, 0, 0, 1, 0, 0, 0, 0],
            [INFER, INFER, 3, 3, 0, 0, 1, 0, 0, 0, 0],
            [400, 400, 4, 4, 2, 2, 3, 2, 1, 1, 0],
            [400, 400, 5, 5, 1, 1, 1, 1, 1, 1, 0],
            [400, 400, 5, 5, 1, 1, 1, 1, 1, 1, 1],
            [INFER, INFER, 6, 6, 1, 1, 1, 1, 1, 1, 1],
        ]

        return args

    @staticmethod
    def generate_component(
            w, h, colsid, rowsid, hspaceid, vspaceid, stroke_width, paddingid, merge_right_id, merge_bot_id, kwargs_gen_id):

        CELL_KWARGS_GENERATOR = [
            TestGrid.kwargs1,
            TestGrid.kwargs2
        ]

        rect = Rectangle(0, 0, 500, 500, stroke_width=0, fill_src=(1, 1, 1, 0.8))

        cols = TestGrid.COLS[colsid]
        rows = TestGrid.ROWS[colsid]

        grid = Grid(
            50, 50, w, h, cols, rows, TestGrid.HSPACE[hspaceid],
            TestGrid.VSPACE[vspaceid], stroke_width=stroke_width, padding=TestGrid.PADDING[paddingid],
            stroke_src=(0, 0.3, 0.6, 1), fill_src=(0.8, 0.5, 0.0, 0.8),
            cell_kwargs_generator=CELL_KWARGS_GENERATOR[kwargs_gen_id]
        )
        rect.add(grid)


        for i, j in TestGrid.MERGE_RIGHT[merge_right_id]:
            grid.cell_merge_right(i, j)

        for i, j in TestGrid.MERGE_BOT[merge_bot_id]:
            grid.cell_merge_down(i, j)

        for i in range(len(rows)):
            for j in range(len(cols)):
                content = Rectangle(3, 3, 15 + i*2, 15 + j*2, stroke_width=1, stroke_src=(0.9, 0.6, 0.3, 1),
                                    fill_src=(0.3, 0.3, 0.6, 0.7))
                if grid.cells[i][j]:
                    grid.add(content, i, j)
                    
        return rect

    def test(self):
        super(TestGrid, self).execute()