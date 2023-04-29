import pytest
from kektris.kektris import Game
from kektris.blocks import Grid, Figure
from kektris.constraints import FigureOrientation
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

    # TODO: remove me
    def test_is_line_grown(self, make_app: Game) -> None:
        """Test is line monotonic grown
        """
        assert make_app._is_line_grown([1, 2, 3, 4, 5]), 'not grown'
        assert not make_app._is_line_grown([1, 2, 3, 5]), 'grown'

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
