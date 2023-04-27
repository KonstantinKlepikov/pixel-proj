from kektris.constraints import (
    Direction,
    Orientation,
    CellState,
    CellPlace,
    FigureOrientation,
    ARRIVE_TOP,
    ARRIVE_BOTTOM,
    ARRIVE_LEFT,
    ARRIVE_RIGHT,
        )
from typing import TypeAlias, Optional


class Cell:
    """This class represent a cell of grid
    """
    pixel_size = 5

    def __init__(
        self, x: int,
        y: int,
        place: CellPlace,
        state: CellState = CellState.CLEAR
            ) -> None:
        self.x = x
        self.y = y
        self.place = place
        self.state = state
        self._pos = (x, y)

    @property
    def pos(self) -> tuple[int]:
        """Return current position
        """
        return self._pos

    @property
    def is_frozen(self) -> bool:
        return self.state == CellState.FR0ZEN

    @property
    def is_clear(self) -> bool:
        return self.state == CellState.CLEAR

    @property
    def is_blocked(self) -> bool:
        return self.state == CellState.BLOCK

    @property
    def is_top_left(self) -> bool:
        return self.place == CellPlace.TOP_LEFT

    @property
    def is_top_right(self) -> bool:
        return self.place == CellPlace.TOP_RIGHT

    @property
    def is_bottom_left(self) -> bool:
        return self.place == CellPlace.BOTTOM_LEFT

    @property
    def is_bottom_right(self) -> bool:
        return self.place == CellPlace.BOTTOM_RIGHT

    def __hash__(self) -> int:
        return hash(self.pos)

    def __eq__(self, other) -> bool:
        if isinstance(other, Cell):
            return self.pos == other.pos
        return NotImplemented

    def freeze(self) -> None:
        """Freeze cell
        """
        self.state = CellState.FR0ZEN

    def clear(self) -> None:
        """Clear the cell
        """
        self.state = CellState.CLEAR

    def block(self) -> None:
        """Block the cell
        """
        self.state = CellState.BLOCK


Cells: TypeAlias = list[list[Cell]]


class Grid:
    """This class represent a grid of cells
    """
    cells = 34
    half = 17

    def __init__(self) -> None:
        self.grid: Cells = self._make_grid()

    def _make_grid(self) -> list[list[Cells]]:
        # TODO: rewrite with list comprehensione
        grid = []
        for x in range(0, self.half):
            row = []
            for y in range(0, self.half):
                row.append(Cell(x, y, place=CellPlace.TOP_LEFT))
            for y in range(self.half, self.cells):
                row.append(Cell(x, y, place=CellPlace.TOP_RIGHT))
            grid.append(row)
        for x in range(self.half, self.cells):
            row = []
            for y in range(0, self.half):
                row.append(Cell(x, y, place=CellPlace.BOTTOM_LEFT))
            for y in range(self.half, self.cells):
                row.append(Cell(x, y, place=CellPlace.BOTTOM_RIGHT))
            grid.append(row)
        return grid

    @property
    def get_clear(self) -> list[Cell]:
        """Get all clear cell
        """
        return [cell for row in self.grid for cell in row if cell.is_clear]

    @property
    def get_frozen(self) -> list[Cell]:
        """Get all froxen cell
        """
        return [cell for row in self.grid for cell in row if cell.is_frozen]

    @property
    def get_blocked(self) -> list[Cell]:
        """Get all blocked
        """
        return [cell for row in self.grid for cell in row if cell.is_blocked]

    def is_clear(self, pos: tuple[int, int]) -> bool:
        """Is cell with given position clear
        """
        return self.grid[pos[0]][pos[1]].is_clear

    def is_frozen(self, pos: tuple[int, int]) -> bool:
        """Is cell with given position frozen
        """
        return self.grid[pos[0]][pos[1]].is_frozen

    def is_blocked(self, pos: tuple[int, int]) -> bool:
        """Is cell with given position blocked
        """
        return self.grid[pos[0]][pos[1]].is_blocked

    def freeze_blocked(self) -> None:
        """Freeze all blocked cells
        """
        [cell.freeze() for cell in self.get_blocked]

    def clear_blocked(self) -> None:
        """Clear all blocked cells
        """
        [cell.clear() for cell in self.get_blocked]


class Window:
    """Represents 4x4 figure window
    """

    def __init__(
        self,
        top_left: tuple[int, int],
        orientation: FigureOrientation,
        grid: Grid,
        move_direction: Optional[Direction] = None,
            ) -> None:
        self.top_left = top_left
        self.orientation = orientation
        self.grid = grid
        if not move_direction:
            self.move_direction: Direction = self._set_move_direction(top_left)
        else:
            self.move_direction = move_direction

    def _set_move_direction(self, top_left: tuple[int, int]) -> Direction:
        """Set move direction
        """
        match top_left:
            case _ if top_left in ARRIVE_LEFT:
                return Direction.RIGHT
            case _ if top_left in ARRIVE_RIGHT:
                return Direction.LEFT
            case _ if top_left in ARRIVE_TOP:
                return Direction.DOWN
            case _ if top_left in ARRIVE_BOTTOM:
                return Direction.UP
        raise ValueError

    def _get_window(self) -> list[list[Cell | None]]:
        """Get window of cells
        """
        result = [[None, None, None, None] for _ in range(4)]
        for row in range(4):
            y = row + self.top_left[1]
            for col in range(4):
                x = col + self.top_left[0]
                if (34 > x >= 0) and (34 > y >= 0):
                    result[row][col] = self.grid.grid[x][y]
        return result

    def map_window(self) -> list[Cell]:
        """Get mapped cell
        """
        result = []
        for maps, cells in zip(self.orientation.value, self._get_window()):
            result.extend([cell for m, cell in zip(maps, cells) if cell and m])
        return result


class Figure:
    """Kektris figure with its current
    orientation and position on the game grid
    """

    def __init__(
        self,
        window: Window,
            ) -> None:
        self.window = window
        self.shape = window.orientation.name[0]

    def move_figure(self, direction: Direction) -> None:
        """Move a figure one step in a given direction
        """
        x, y = self.window.top_left
        match direction, self.window.move_direction:
            case Direction.LEFT, d if d != Direction.RIGHT:
                new_window = Window(
                    (x-1, y),
                    self.window.orientation,
                    self.window.grid,
                    self.window.move_direction
                        )
            case Direction.RIGHT, d if d != Direction.LEFT:
                new_window = Window(
                    (x+1, y),
                    self.window.orientation,
                    self.window.grid,
                    self.window.move_direction
                        )
            case Direction.UP, d if d != Direction.DOWN:
                new_window = Window(
                    (x, y-1),
                    self.window.orientation,
                    self.window.grid,
                    self.window.move_direction
                        )
            case Direction.DOWN, d if d != Direction.UP:
                new_window = Window(
                    (x, y+1),
                    self.window.orientation,
                    self.window.grid,
                    self.window.move_direction
                        )
            case _, _:
                return
        self.block_figure(new_window)

    def rotate_figure(self, direction: Direction) -> None:
        """Rotates a figure in a given rotation side
        """
        if self.window.orientation == FigureOrientation.O:
            return

        new_window = Window(
            self.window.top_left,
            FigureOrientation[
                self.shape + '_' + self._choose_orientation(direction).name
                    ],
            self.window.grid,
            self.window.move_direction
                )
        self.block_figure(new_window)

    def _choose_orientation(self, direction: Direction) -> Orientation:
        """Choose orientation of figure after rotation
        """
        try:
            orientation = self.window.orientation.name[2]
        except IndexError:
            raise ValueError('Is a squire! It havent orientation!')

        ind = Orientation[orientation].value
        match direction, ind:
            case Direction.RIGHT, 4:
                return Orientation(1)
            case Direction.RIGHT, o if o < 4:
                return Orientation(ind+1)
            case Direction.LEFT, 1:
                return Orientation(4)
            case Direction.LEFT, o if o > 1:
                return Orientation(ind-1)
            case _:
                raise ValueError('Wrong direction!')

    def block_figure(self, window: Window) -> None:
        """Block cells for figure
        """
        cells = window.map_window()
        if self.is_valid_figure(cells):
            self.window.grid.clear_blocked()
            [self.window.grid.grid[cell.x][cell.y].block() for cell in cells]
            self.window = window

    def is_valid_figure(
        self,
        cells: list[Cell],
            ) -> bool:
        """"Returns true if all the tiles of the block are valid
        i.e. on the grid and doesn't occupy already filled tiles
        """
        return all([not cell.is_frozen for cell in cells])
