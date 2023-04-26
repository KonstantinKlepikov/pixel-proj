import random
from kektris.constraints import (
    Direction,
    Shape,
    Orientation,
    BlockOrientation,
    CellState,
    CellPlace,
    FigureOrientation
        )
from typing import Optional, TypeAlias


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
            ) -> None:
        self.top_left = top_left
        self.orientation = orientation
        self.grid = grid

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
        match direction:
            case Direction.LEFT:
                new_window = Window(
                    (x-1, y),
                    self.window.orientation,
                    self.window.grid
                        )
            case Direction.RIGHT:
                new_window = Window(
                    (x+1, y),
                    self.window.orientation,
                    self.window.grid
                        )
            case Direction.UP:
                new_window = Window(
                    (x, y-1),
                    self.window.orientation,
                    self.window.grid
                        )
            case Direction.DOWN:
                new_window = Window(
                    (x, y+1),
                    self.window.orientation,
                    self.window.grid
                        )
        self.block_figure(new_window)

    def rotate_figure(self, direction: Direction) -> None:
        """Rotates a figure in a given rotation side
        """
        match direction:
            case Direction.LEFT:
                new_window = Window(
                    self.window.top_left,
                    FigureOrientation[self.shape + '_' + Orientation.U.name],
                    self.window.grid
                        )
            case Direction.RIGHT:
                new_window = Window(
                    self.window.top_left,
                    FigureOrientation[self.shape + '_' + Orientation.D.name],
                    self.window.grid
                        )
            case Direction.UP:
                new_window = Window(
                    self.window.top_left,
                    FigureOrientation[self.shape + '_' + Orientation.R.name],
                    self.window.grid
                        )
            case Direction.DOWN:
                new_window = Window(
                    self.window.top_left,
                    FigureOrientation[self.shape + '_' + Orientation.L.name],
                    self.window.grid
                        )
        self.block_figure(new_window)

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
        return all([cell.is_clear for cell in cells])


class Block:
    """Kektris block with its current
    orientation and position on the game grid
    """

    def __init__(self, shape: Optional[int] = None) -> None:
        self.orientation = 0
        if shape != None:
            self.shape = shape
        else:
            self.shape = random.randint(0, 6)
        self.position: tuple[int, int] = (0, 3)

    def move_block(
        self,
        direction: Optional[Direction],
        grid: list[int],
            ) -> Optional[bool]:
        """Move a block one step in a given direction
        """
        if direction == None:
            return

        if direction == Direction.LEFT:
            new_position = (self.position[0], self.position[1] - 1)
        elif direction == Direction.RIGHT:
            new_position = (self.position[0], self.position[1] + 1)
        elif direction == Direction.UP:
            new_position = (self.position[0] - 1, self.position[1])
        elif direction == Direction.DOWN:
            new_position = (self.position[0] + 1, self.position[1])

        if self.is_valid_block(
            self.get_block_tiles(new_position, self.orientation), grid
                ):
            self.position = new_position
            return True

        return False

    def rotate_block(
        self,
        direction: Optional[Direction],
        grid: list[int],
            ) -> Optional[bool]:
        """Rotates a block in a given rotation side
        """
        if direction == None:
            return

        n_orient = (self.orientation + 1) % 4 if direction == Direction.RIGHT \
            else (self.orientation - 1) % 4
        if self.is_valid_block(
            self.get_block_tiles(self.position, n_orient), grid
                ):
            self.orientation = n_orient
            return True

        return False

    def is_valid_block(
        self,
        block_tiles: set[tuple],
        grid: list[int],
            ) -> bool:
        """"Returns true if all the tiles of the block are valid
        i.e. on the grid and doesn't occupy already filled tiles
        """
        for tile in block_tiles:
            if not(0 <= tile[0] <= 21) \
                    or not(0 <= tile[1] <= 9) \
                    or grid[tile[0]][tile[1]] != 0:
                return False
        return True

    def get_block_tiles(
        self,
        position: tuple[int, int],
        orientation: int
            ) -> set[tuple[int, int]]:
        """Get oriented block
        """
        block_name = Shape(self.shape).name + '_' + Orientation(orientation).name
        block_tiles = BlockOrientation[block_name].value
        return {
            (tile[0] + position[0], tile[1] + position[1]) for tile in block_tiles
                }
