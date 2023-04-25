import pytest
from kektris.blocks import Cell, Grid, Figure, FigureWindow
from kektris.constraints import CellPlace, FigureOrientation


@pytest.fixture(scope='function')
def grid() -> Grid:
    return Grid()


class TestCell:
    """Test Cell class
    """

    @pytest.fixture(scope='function')
    def cell(self) -> Cell:
        """Cell fixture
        """
        return Cell(0, 0, CellPlace.TOP_LEFT)

    def test_cell_position(self, cell: Cell) -> None:
        """Test cell position
        """
        assert cell.pos == (0, 0), 'wrong position'
        cell.x = 55
        assert cell.pos == (0, 0), 'wrong position'

    def test_cell_state(self, cell: Cell) -> None:
        """Test cell clear
        """
        cell.freeze()
        assert cell.is_frozen, 'wrong state'
        assert not cell.is_clear, 'wrong state'
        assert not cell.is_blocked, 'wrong state'
        cell.block()
        assert not cell.is_frozen, 'wrong state'
        assert not cell.is_clear, 'wrong state'
        assert cell.is_blocked, 'wrong state'
        cell.clear()
        assert cell.is_clear, 'wrong state'
        assert not cell.is_frozen, 'wrong state'
        assert not cell.is_blocked, 'wrong state'

    def test_cell_place(self, cell: Cell) -> None:
        """Test cell place
        """
        assert cell.is_top_left, 'wrong place'
        cell.place = CellPlace.TOP_RIGHT
        assert cell.is_top_right, 'wrong place'
        cell.place = CellPlace.BOTTOM_LEFT
        assert cell.is_bottom_left, 'wrong place'
        cell.place = CellPlace.BOTTOM_RIGHT
        assert cell.is_bottom_right, 'wrong place'

    def test_cell_eq(self, cell: Cell) -> None:
        """Test cell equality
        """
        another = Cell(0, 1, CellPlace.TOP_LEFT)
        assert cell != another, 'is equal'
        another = Cell(0, 0, CellPlace.TOP_LEFT)
        assert cell == another, 'is not equal'
        assert not (cell == 'not cell'), 'wrong eq return'


class TestGrid:
    """Test Grid class
    """

    def test_grid_init(self, grid: Grid) -> None:
        """Test Grid initialization
        """
        assert grid.cells == 34, 'wrong cells number'
        assert grid.half == 17, 'wrong half cels number'
        assert isinstance(grid.grid, list), 'wtong grid type'
        assert len(grid.grid) == 34, 'wrong row number'
        assert len(grid.grid[0]) == 34, 'wrong col number'
        assert isinstance(grid.grid[0][0], Cell), 'wrong cell'
        assert grid.grid[0][0].pos == (0, 0), 'wrong cell pos'
        assert grid.grid[0][0].is_top_left, 'wrong place'
        assert grid.grid[0][17].pos == (0, 17), 'wrong cell pos'
        assert grid.grid[0][17].is_top_right, 'wrong place'
        assert grid.grid[17][0].pos == (17, 0), 'wrong cell pos'
        assert grid.grid[17][0].is_bottom_left, 'wrong place'
        assert grid.grid[17][17].pos == (17, 17), 'wrong cell pos'
        assert grid.grid[17][17].is_bottom_right, 'wrong place'

    def test_get_clear(self, grid: Grid) -> None:
        """Test get clear
        """
        assert len(grid.get_clear) == 34 * 34, 'wrong clear cells len'
        grid.grid[0][0].block()
        assert len(grid.get_clear) == 34 * 34 - 1, 'wrong clear cells len'
        assert grid.grid[0][0] not in grid.get_clear, 'wrong clear cells number'

    def test_get_frozen(self, grid: Grid) -> None:
        """Test get frozen
        """
        assert len(grid.get_frozen) == 0, 'wrong frozen cells len'
        grid.grid[0][0].freeze()
        assert len(grid.get_frozen) == 1, 'wrong frozen cells len'
        assert grid.grid[0][0] in grid.get_frozen, 'wrong frozen cells number'

    def test_get_blocked(self, grid: Grid) -> None:
        """Test get blocked
        """
        assert len(grid.get_blocked) == 0, 'wrong blocked cells len'
        grid.grid[0][0].block()
        assert len(grid.get_blocked) == 1, 'wrong blocked cells len'
        assert grid.grid[0][0] in grid.get_blocked, 'wrong blocked cels number'

    def test_is_clear(self, grid: Grid) -> None:
        """Test is cell clear
        """
        assert grid.is_clear((0, 0)), 'not clear'
        grid.grid[0][0].block()
        assert not grid.is_clear((0, 0)), 'clear'

    def test_is_frozen(self, grid: Grid) -> None:
        """Test is cell frozen
        """
        assert not grid.is_frozen((0, 0)), 'frozen'
        grid.grid[0][0].freeze()
        assert grid.is_frozen((0, 0)), 'not frozen'

    def test_is_blocked(self, grid: Grid) -> None:
        """Test is cell blocked
        """
        assert not grid.is_blocked((0, 0)), 'blocked'
        grid.grid[0][0].block()
        assert grid.is_blocked((0, 0)), 'not blocked'

    def test_clear_blocked(self, grid: Grid) -> None:
        """Test clear blocked
        """
        grid.grid[0][0].block()
        assert len(grid.get_clear) == 34 * 34 - 1, 'wrong clear cells len'
        assert len(grid.get_blocked) == 1, 'wrong blocked cells len'
        grid.clear_blocked()
        assert len(grid.get_clear) == 34 * 34, 'wrong clear cells len'
        assert len(grid.get_blocked) == 0, 'wrong blocked cells len'

    def test_freeze_blocked(self, grid: Grid) -> None:
        """Test freeze blocked
        """
        grid.grid[0][0].block()
        assert len(grid.get_clear) == 34 * 34 - 1, 'wrong clear cells len'
        assert len(grid.get_blocked) == 1, 'wrong blocked cells len'
        assert len(grid.get_frozen) == 0, 'wrong frozen cells len'
        grid.freeze_blocked()
        assert len(grid.get_clear) == 34 * 34 - 1, 'wrong clear cells len'
        assert len(grid.get_blocked) == 0, 'wrong blocked cells len'
        assert len(grid.get_frozen) == 1, 'wrong frozen cells len'


class TestFigureWindow:
    """Test FigureWinfow class
    """

    def test_window_get_window(self, grid: Grid) -> None:
        """Test get_window
        """
        window = FigureWindow((0, 0), FigureOrientation.I_L, grid)
        w = window._get_window()
        assert isinstance(w, list), 'wrong result type'
        assert len(w) == 4, 'wrong result len'
        assert isinstance(w[0], list), 'wrong inside type'
        assert len(w[0]) == 4, 'wrong inside len'
        assert isinstance(w[0][0], Cell), 'wrong cell type'
        assert w[0][0].pos == window.grid.grid[0][0].pos, 'wrong cell value'

    def test_window_get_ofgrid_left_window(self, grid: Grid) -> None:
        """Test get_window ofboard from top left
        """
        window = FigureWindow((-1, -1), FigureOrientation.I_L, grid)
        w = window._get_window()
        assert w[0][0] == None, 'wrong ofgrid cell value'
        assert w[1][0] == None, 'wrong ofgrid cell value'
        assert w[0][1] == None, 'wrong ofgrid cell value'
        assert w[1][1].pos == window.grid.grid[0][0].pos, 'wrong grid cell value'

    def test_window_get_ofgrid_right_window(self, grid: Grid) -> None:
        """Test get_window ofboard from bottom right
        """
        window = FigureWindow((33, 33), FigureOrientation.I_L, grid)
        w = window._get_window()
        assert w[1][0] == None, 'wrong ofgrid cell value'
        assert w[0][1] == None, 'wrong ofgrid cell value'
        assert w[0][0].pos == window.grid.grid[33][33].pos, 'wrong grid cell value'

    def test_map_window(self, grid: Grid) -> None:
        """Test msp window return cells
        """
        window = FigureWindow((0, 0), FigureOrientation.I_L, grid)
        m = window.map_window()
        assert isinstance(m, list), 'wrong result type'
        assert len(m) == 4, 'wrong result len'
        assert isinstance(m[0], Cell), 'wrong cell type'
        assert m[0].pos == grid.grid[1][0].pos, 'wrong figure'
        assert m[1].pos == grid.grid[1][1].pos, 'wrong figure'

    def test_map_window_ofgrid_left_window(self, grid: Grid) -> None:
        """Test msp window return cells with ofboard from top left
        """
        window = FigureWindow((-1, 0), FigureOrientation.I_U, grid)
        m = window.map_window()
        assert len(m) == 3, 'wrong result len'
        assert m[0].pos == grid.grid[0][1].pos, 'wrong figure'
        assert m[1].pos == grid.grid[1][1].pos, 'wrong figure'

    def test_map_window_ofgrid_right_window(self, grid: Grid) -> None:
        """Test msp window return cells with ofboard from ищеещь кшпре
        """
        window = FigureWindow((33, 31), FigureOrientation.I_U, grid)
        m = window.map_window()
        assert len(m) == 1, 'wrong result len'
        assert m[0].pos == grid.grid[33][32].pos, 'wrong figure'


class TestFigure:
    """Test figure class
    """
