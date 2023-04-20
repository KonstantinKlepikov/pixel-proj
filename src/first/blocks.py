import random
from constraints import (
    Direction,
    Shape,
    Orientation,
    BlockOrientation,
        )
from typing import Optional


class Block():
    """Kektris block with its current
    orientation and position on the game grid
    """

    def __init__(self, shape: Optional[int] = None) -> None:
        self.orientation = 0
        if shape != None:
            self.shape = shape
        else:
            self.shape = random.randint(0, 6)
        self.position = (0, 3)

    def move_block(
        self,
        direction: Optional[Direction],
        grid
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
            self.get_block_tiles(new_position, self.orientation),
            grid
                ):
            self.position = new_position
            return True

        return False

    def rotate_block(
        self,
        direction: Optional[Direction],
        grid
            ) -> Optional[bool]:
        """Rotates a block in a given rotation side
        """
        if direction == None:
            return

        n_orient = (self.orientation + 1) % 4 if direction == Direction.RIGHT \
            else (self.orientation - 1) % 4
        if self.is_valid_block(
            self.get_block_tiles(self.position, n_orient),
            grid
                ):
            self.orientation = n_orient
            return True

        return False

    def is_valid_block(self, block_tiles: set[tuple], grid) -> bool:
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
            ) -> set[tuple]:
        """Get oriented block
        """
        block_name = Shape(self.shape).name + '_' + Orientation(orientation).name
        block_tiles = BlockOrientation[block_name].value
        return {
            (tile[0] + position[0], tile[1] + position[1]) for tile in block_tiles
                }
