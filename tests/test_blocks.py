import pytest
from kektris.blocks import Cell, Grid, Block
from kektris.constraints import CellPlace


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
