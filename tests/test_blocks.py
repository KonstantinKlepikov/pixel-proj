import pytest
from kektris.blocks import Cell, Grid, Figure, Window
from kektris.constraints import (
    FigureOrientation,
    Direction,
        )


class TestCell:
    """Test Cell class
    """

    @pytest.fixture(scope='function')
    def cell(self) -> Cell:
        """Cell fixture
        """
        return Cell(0, 0)

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

    def test_cell_eq(self, cell: Cell) -> None:
        """Test cell equality
        """
        another = Cell(0, 1)
        assert cell != another, 'is equal'
        another = Cell(0, 0)
        assert cell == another, 'is not equal'
        assert not (cell == 'not cell'), 'wrong eq return'


class TestGrid:
    """Test Grid class
    """

    def test_grid_init(self, grid: Grid) -> None:
        """Test Grid initialization
        """
        assert grid.cells == 34, 'wrong cells number'
        assert isinstance(grid.grid, list), 'wtong grid type'
        assert len(grid.grid) == 34, 'wrong row number'
        assert len(grid.grid[0]) == 34, 'wrong col number'
        assert isinstance(grid.grid[0][0], Cell), 'wrong cell'
        assert grid.grid[0][0].pos == (0, 0), 'wrong cell pos'
        assert grid.grid[0][17].pos == (0, 17), 'wrong cell pos'
        assert grid.grid[17][0].pos == (17, 0), 'wrong cell pos'
        assert grid.grid[17][17].pos == (17, 17), 'wrong cell pos'

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


class TestWindow:
    """Test FigureWinfow class
    """

    @pytest.mark.parametrize(
        'direction,arrive_pos', [
            (Direction.RIGHT, (-4, 0)),
            (Direction.LEFT, (34, 0)),
            (Direction.UP, (0, 34)),
            (Direction.DOWN, (0, -4))
                ]
            )
    def test_set_move_direction(
        self,
        grid: Grid,
        arrive_pos: tuple[int, int],
        direction: Direction
            ) -> None:
        """Test get_window
        """
        window = Window(arrive_pos, FigureOrientation.I_L, grid)
        assert window.move_direction == direction, 'wrong direction'

    def test_window_not_created_in_a_wrong_side(self, grid: Grid) -> None:
        """Test raise error with window creation
        """
        with pytest.raises(ValueError):
            Window((0, 0), FigureOrientation.I_L, grid)

    def test_window_get_window(self, grid: Grid) -> None:
        """Test get_window
        """
        window = Window((0, 0), FigureOrientation.I_L, grid, Direction.LEFT)
        w = window.get_window
        assert isinstance(w, list), 'wrong result type'
        assert len(w) == 4, 'wrong result len'
        assert isinstance(w[0], list), 'wrong inside type'
        assert len(w[0]) == 4, 'wrong inside len'
        assert isinstance(w[0][0], Cell), 'wrong cell type'
        assert w[0][0].pos == window.grid.grid[0][0].pos, 'wrong cell value'

    def test_window_get_ofgrid_left_window(self, grid: Grid) -> None:
        """Test get_window ofboard from top left
        """
        window = Window((-1, -1), FigureOrientation.I_L, grid, Direction.LEFT)
        w = window.get_window
        assert w[0][0] == None, 'wrong ofgrid cell value'
        assert w[1][0] == None, 'wrong ofgrid cell value'
        assert w[0][1] == None, 'wrong ofgrid cell value'
        assert w[1][1].pos == window.grid.grid[0][0].pos, 'wrong grid cell value'

    def test_window_get_ofgrid_right_window(self, grid: Grid) -> None:
        """Test get_window ofboard from bottom right
        """
        window = Window((33, 33), FigureOrientation.I_L, grid, Direction.LEFT)
        w = window.get_window
        assert w[1][0] == None, 'wrong ofgrid cell value'
        assert w[0][1] == None, 'wrong ofgrid cell value'
        assert w[0][0].pos == window.grid.grid[33][33].pos, 'wrong grid cell value'

    def test_map_window(self, grid: Grid) -> None:
        """Test msp window return cells
        """
        window = Window((0, 0), FigureOrientation.I_L, grid, Direction.LEFT)
        m = window.map_window
        assert isinstance(m, list), 'wrong result type'
        assert len(m) == 4, 'wrong result len'
        assert isinstance(m[0], Cell), 'wrong cell type'
        assert m[0].pos == grid.grid[1][0].pos, 'wrong figure'
        assert m[1].pos == grid.grid[1][1].pos, 'wrong figure'

    def test_map_window_ofgrid_left_window(self, grid: Grid) -> None:
        """Test msp window return cells with ofboard from top left
        """
        window = Window((-1, 0), FigureOrientation.I_U, grid, Direction.LEFT)
        m = window.map_window
        assert len(m) == 3, 'wrong result len'
        assert m[0].pos == grid.grid[0][1].pos, 'wrong figure'
        assert m[1].pos == grid.grid[1][1].pos, 'wrong figure'

    def test_map_window_ofgrid_right_window(self, grid: Grid) -> None:
        """Test msp window return cells with ofboard from ищеещь кшпре
        """
        window = Window((33, 31), FigureOrientation.I_U, grid, Direction.LEFT)
        m = window.map_window
        assert len(m) == 1, 'wrong result len'
        assert m[0].pos == grid.grid[33][32].pos, 'wrong figure'

    def test_has_frozen(self, grid: Grid) -> None:
        """Test has frozen mapped window

        Args:
            grid (Grid): _description_
        """
        window = Window((0, 0), FigureOrientation.I_L, grid, Direction.LEFT)
        assert not window.has_frozen(), 'has frozen'
        window = Window((0, 0), FigureOrientation.I_U, grid, Direction.LEFT)
        window.grid.grid[1][1].freeze()
        assert window.has_frozen(), 'not has frozen'


class TestFigure:
    """Test figure class
    """

    @pytest.fixture(scope='function', params=FigureOrientation.get_includes())
    def window(self, grid: Grid, request) -> Window:
        """Make window
        """
        window = Window((0, 0), request.param, grid, Direction.LEFT)
        window.param = request.param
        return window

    @pytest.fixture(scope='function')
    def figure(self, window: Window) -> Figure:
        """Make figure
        """
        return Figure(window)

    def test_figure_init(self, figure: Figure) -> None:
        """Test figure initialization
        """
        assert figure.shape == figure.window.param.name[0], 'wrong shape'

    def test_is_valid_figure(self, figure: Figure) -> None:
        """Test is_valid_figure method
        """
        assert figure.is_valid_figure(figure.window), 'not valid'

    def test_is_valid_figure_has_frozen(self, figure: Figure, grid: Grid) -> None:
        """Test is_valid_figure method
        """
        grid.grid[1][1].freeze()
        grid.grid[2][2].freeze()
        grid.grid[3][3].freeze()
        assert not figure.is_valid_figure(figure.window), 'valid'

    def test_block_figure(
        self,
        figure: Figure,
        window: Window,
            ) -> None:
        """Test block figure
        """
        figure.block_figure(window)
        assert figure.window.grid.get_blocked, 'not blocked'

    def test_clear_before_block(
        self,
        figure: Figure,
        window: Window,
            ) -> None:
        """Test block figure and clear before block
        """
        figure.window.grid.grid[33][33].block()
        figure.block_figure(window)
        assert figure.window.grid.get_blocked, 'not blocked'
        assert figure.window.grid.grid[33][33].is_clear, 'not clear'

    # TODO: rewrite me for all params
    def test_is_ready_for_freeze_figure(self, grid: Grid) -> None:
        """Test freeze figure
        """
        window = Window((16, 0), FigureOrientation.O, grid, Direction.LEFT)
        figure = Figure(window)
        figure.block_figure(figure.window)
        assert figure.is_ready_for_freeze_figure(), 'wrong get blocked'

    @pytest.mark.parametrize(
        'direction,result', [
            (Direction.LEFT, (-1, 0)),
            (Direction.RIGHT, (1, 0)),
            (Direction.DOWN, (0, 1)),
            (Direction.UP, (0, -1))
                ]
            )
    def test_move_figure(
        self,
        figure: Figure,
        direction: Direction,
        result: tuple[int, int],
            ) -> None:
        """Test figure moving
        """
        window = figure.move_figure(direction)
        if (direction == Direction.UP and figure.window.move_direction != Direction.DOWN) \
            or (direction == Direction.DOWN and figure.window.move_direction != Direction.UP) \
            or (direction == Direction.RIGHT and figure.window.move_direction != Direction.LEFT) \
            or (direction == Direction.LEFT and figure.window.move_direction != Direction.RIGHT):
            assert window.top_left == result, 'not moved'
        else:
            assert not window, 'moved to not accepted side'

    def test_choose_orientation_raise_if_squire(self, grid: Grid) -> None:
        """Test choose orientation raise if squire
        """
        window = Window((0, 0), FigureOrientation.O, grid, Direction.LEFT)
        figure = Figure(window)
        with pytest.raises(
            ValueError,
            match='Is a squire! It havent orientation!'
                ):
            figure._choose_orientation(Direction.RIGHT)

    def test_choose_orientation_raise_if_wrong_direction(self, grid: Grid) -> None:
        """Test choose orientation raise if wrong direction
        """
        window = Window((0, 0), FigureOrientation.I_D, grid, Direction.LEFT)
        figure = Figure(window)
        with pytest.raises(
            ValueError,
            match='Wrong direction!'
                ):
            figure._choose_orientation(Direction.DOWN)

    @pytest.mark.skip('TODO: add me')
    def test_choose_orientation(self, grid: Grid) -> None:
        """Test choose orientation
        """

    @pytest.mark.skip('TODO: rewrite me')
    @pytest.mark.parametrize(
        'direction,result', [
            (Direction.LEFT, 'U'),
            (Direction.RIGHT, 'D'),
                ]
            )
    def test_rotate_figure(
        self,
        figure: Figure,
        direction: Direction,
        result: str,
            ) -> None:
        """Test rotate figure
        """
        figure.rotate_figure(direction)
        assert figure.window.top_left == (0, 0), 'wrong top left'
        if figure.window.orientation.name != 'O':  # case with square apriory done
            assert figure.window.orientation.name[2] == result, \
                'wrong orientation'
