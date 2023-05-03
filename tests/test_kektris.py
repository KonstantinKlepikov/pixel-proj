import pytest
from kektris.kektris import Game
from kektris.blocks import Grid, Figure, Window
from kektris.constraints import FigureOrientation, Direction
from conftest import FixedSeed


class TestGame:
    """Test game interfaces
    """

    def test_app_init(self, make_app: Game) -> None:
        """Test app init
        """
        assert make_app.paused, 'not paused'
        assert make_app.score == 0, 'wrong score'
        assert make_app.speed == 0, 'wrong speed'
        assert isinstance(make_app.grid, Grid), 'wrong grid'
        assert not make_app.grid_higlight, 'grid highlited'

    def test_generate_figure_start_position(self, make_app: Game) -> None:
        """Test random figure generation
        """
        with FixedSeed(42):
            top_left, orientation = make_app._generate_figure_start_position()
            assert isinstance(top_left, tuple), 'wrong result'
            assert top_left == (-4, 21), 'wrong top left position'
            assert orientation == FigureOrientation.I_R, 'wrong orientation'

    def test_arrive_figure(self, make_app: Game) -> None:
        """Test arrive figure
        """
        with FixedSeed(42):
            figure = make_app._arrive_figure()
            assert isinstance(figure, Figure), 'wrong figure move_direction'
            assert figure.window.top_left == (-4, 21), \
                'wrong top left position'
            assert figure.window.orientation == FigureOrientation.I_R, \
                'wrong orientation'

    def test_get_chunked(self, make_app: Game) -> None:
        """Test get chunked
        """
        i = [1, 2, 3]
        line, chunked = make_app._get_chunked(i, [])
        assert not line, 'line nt empty'
        assert isinstance(line, list), 'wrong line type'
        assert isinstance(chunked, list), 'wrong chunked type'
        assert len(chunked) == 1, 'wrong chunked len'
        assert chunked[0] == [3, 2, 1], 'wrong chunk'

    @pytest.mark.parametrize(
        'i,ch', [
            ([1, 2, 3, 4, 5, 6, 8, 9], [[6, 5, 4, 3, 2, 1], [9, 8]]),
            ([1, 3], [[1], [3]]),
                    ]
                )
    def test_get_chunked_parts(self, make_app: Game, i: list[int], ch: list[list[int]]) -> None:
        """Test get chunked multiple parts
        """
        line, chunked = make_app._get_chunked(i, [])
        assert not line, 'line nt empty'
        assert isinstance(line, list), 'wrong line type'
        assert isinstance(chunked, list), 'wrong chunked type'
        assert len(chunked) == 2, 'wrong chunked len'
        assert isinstance(chunked[0], list), 'wrong chunk type'
        assert chunked[0] == ch[0], 'wrong chunked'
        assert chunked[1] == ch[1], 'wrong chunked'

    def test_check_line(self, make_app: Game) -> None:
        """Test is line is ready to clear
        """
        for p in range(17):
            make_app.grid.grid[p][0].freeze()
        frozen_pos = [p.pos for p in make_app.grid.get_frozen]
        assert len(make_app.grid.get_frozen) == 17, 'wrong frozen'
        line = make_app._check_line(1, frozen_pos)
        assert isinstance(line, list), 'wrong line type'
        assert isinstance(line[0], tuple), 'wrong pos'
        assert len(line) == 17, 'wrong line lenght'
        assert frozen_pos == line, 'wrong comparison'

    def test_check_line_parts(self, make_app: Game) -> None:
        """Test is line is ready to clear if parts
        """
        for p in range(12):
            make_app.grid.grid[p][0].freeze()
        for p in range(14, 17):
            make_app.grid.grid[p][0].freeze()
        frozen_pos = [p.pos for p in make_app.grid.get_frozen]
        assert len(make_app.grid.get_frozen) == 15, 'wrong frozen'
        line = make_app._check_line(1, frozen_pos)
        assert isinstance(line, list), 'wrong line type'
        assert isinstance(line[0], tuple), 'wrong pos'
        assert len(line) == 12, 'wrong line lenght'
        assert frozen_pos[0:12] == line, 'wrong comparison'

    # TODO: remove me
    # def test_line_orientation(self, make_app: Game) -> None:
    #     """Test line orientation
    #     """
    #     assert make_app._line_orientation([(0, 0), (0, 1)]) == Axis.Y, \
    #         'wrong orientation'
    #     assert make_app._line_orientation([(0, 0), (1, 0)]) == Axis.X, \
    #         'wrong orientation'
    #     with pytest.raises(
    #         ValueError,
    #         match="Isn't line!"
    #             ):
    #         make_app._line_orientation([(0, 0), (1, 1)])

    # TODO: remove me
    # def test_move_frozen(self, make_app: Game, grid: Grid) -> None:
    #     """Test move frozen
    #     """
    #     window = Window((0, 0), FigureOrientation.J_L, grid, Direction.RIGHT)
    #     make_app.grid = grid
    #     make_app.figure = Figure(window)
    #     make_app.figure.block_figure(window)
    #     make_app.figure.set_cells_move_direction()
    #     make_app.figure.window.grid.freeze_blocked()
    #     frozen_to_move = make_app.grid.get_frozen
    #     make_app._move_frozen(frozen_to_move)
    #     result = make_app.grid.get_frozen
    #     assert len(result) == 4, 'wrong len of frozen'
    #     assert [cell.pos for cell in result] == [(15,0),(16,0),(16,1),(16,2)], \
    #         'wrong result'

    def test_change_speed(self, make_app: Game) -> None:
        """Test change speed
        """
        make_app._change_speed()
        assert make_app.speed == 0, 'mistaken grown'
        make_app.score = 1000
        make_app._change_speed()
        assert make_app.speed == 1, 'not grown'
        assert make_app.speed_color_timeout == 60, 'wrong timout'
