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
            assert orientation == FigureOrientation.I_D, 'wrong orientation'

    def test_arrive_figure(self, make_app: Game) -> None:
        """Test arrive figure
        """
        with FixedSeed(42):
            figure = make_app.arrive_figure()
            assert isinstance(figure, Figure), 'wrong figure move_direction'
            assert figure.window.top_left == (-4, 21), \
                'wrong top left position'
            assert figure.window.orientation == FigureOrientation.I_D, \
                'wrong orientation'

