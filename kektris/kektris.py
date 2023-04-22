import pyxel
import random
from kektris.blocks import Block, Cell, Grid
from kektris.constraints import Direction, Shape


class App:
    def __init__(self) -> None:
        pyxel.init(256, 256, title="Kektris")
        pyxel.load('blocks.pyxres', image=True)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self) -> None:
        """Reset game state
        """
        self.paused = True
        self.score = 0
        self.speed = 0
        self.score_color_timeout = 60
        self.speed_color_timeout = 60

        self.grid: list[int] = []
        self._grid: Grid = Grid()
        self.grid_higlight = False

        self.frame_count_from_last_move = 0
        self.blocks = Shape.get_values()
        self.grid_tile_colors: list[int] = []
        self.set_gtid_start_state()
        self.set_block()

    def draw(self) -> None:
        """Draw current screen
        """
        pyxel.cls(0)
        pyxel.rectb(10, 10, 205, 205, 1)

        pyxel.text(219, 20, "SCORE", 10)
        pyxel.text(219, 30, str(self.score), self.set_color("score_color_timeout"))

        pyxel.text(219, 50, "SPEED", 10)
        pyxel.text(219, 60, str(self.speed), self.set_color("speed_color_timeout"))

        pyxel.text(20, 226, "Q:quit", 8)

        pyxel.text(50, 226, "R:restart", 9)

        pyxel.text(88, 226, ">", self.hide_reveal(self.paused))
        pyxel.text(92, 226, "P:pause", 12)

        pyxel.text(122, 226, ">", self.hide_reveal(self.grid_higlight))
        pyxel.text(126, 226, "G:greed", 12)

        self.mark_grid()
        self.draw_grid()

    def update(self) -> None:
        """Update current game state
        """
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
            return

        if pyxel.btnp(pyxel.KEY_P):
            if self.paused:
                self.paused = False
            else:
                self.paused = True

        if pyxel.btnp(pyxel.KEY_G):
            if self.grid_higlight:
                self.grid_higlight = False
            else:
                self.grid_higlight = True

        if self.paused:
            return

        move_direction = None
        rotate_direction = None
        fall_center = False
        if pyxel.btnp(pyxel.KEY_LEFT, 12, 2):
            move_direction = Direction.LEFT
        elif pyxel.btnp(pyxel.KEY_RIGHT ,12, 2):
            move_direction = Direction.RIGHT
        elif pyxel.btnp(pyxel.KEY_DOWN ,12, 2):
            move_direction = Direction.DOWN
        elif pyxel.btnp(pyxel.KEY_UP ,12, 2):
            move_direction = Direction.UP
        elif pyxel.btnp(pyxel.KEY_Z ,12, 20):
            rotate_direction = Direction.LEFT
        elif pyxel.btnp(pyxel.KEY_C ,12, 20):
            rotate_direction = Direction.RIGHT
        elif pyxel.btnp(pyxel.KEY_X ,12, 20):
            fall_center = True

        # if fall center and move was successful;
        # reset the frames count from last move
        if self.block.move_block(move_direction, self.grid) and fall_center:
            self.frame_count_from_last_move = 0

        self.block.rotate_block(rotate_direction, self.grid)

        # check if X numbers of frames have elapsed.
        # Then move down if possible, else freeze the block
        # (spawn new block) and reset the frame elapsed
        if (self.frame_count_from_last_move == 45):
            self.frame_count_from_last_move = 0
            if not(self.block.move_block(Direction.DOWN, self.grid)):
                if self.is_game_over():
                    self.reset()
                    return
                self.freeze_block()
                self.clear_rows()
                if (len(self.blocks) == 0):
                    self.blocks = Shape.get_values()
                self.set_block()

        self.frame_count_from_last_move += 1

    def mark_grid(self) -> None:
        """Draw grid mark
        """
        if self.grid_higlight:
            for p in range(10, 217, 6):
                color = 13 if p != 112 else 15
                pyxel.line(p, 10, p, 214, color)
                pyxel.line(10, p, 214, p, color)

    def set_gtid_start_state(self) -> None:
        """Set grid start state
        """
        for _ in range(34):
            self.grid.append([0] * 34)
            self.grid_tile_colors.append([-1] * 34)

    def draw_grid(self) -> None:
        """Draw grid
        """
        current_block_tiles = self.block.get_block_tiles(
            self.block.position, self.block.orientation
                )

        # draw block
        for tile in current_block_tiles:
            if 2 <= tile[0] <= 21:
                pyxel.blt(
                    x=tile[1] * 8 + 21,
                    y=21 + (tile[0] - 2) * 8,
                    img=0,
                    u=self.block.shape * 8,
                    v=0,
                    w=8,
                    h=8,
                    colkey=0
                        )

        # frozen grid
        for row in range(2, 22):
            for column in range(10):
                if self.grid[row][column] == 1:
                    pyxel.blt(21 + column * 8, 21 + (row - 2) * 8, 0, self.grid_tile_colors[row][column] * 8, 0, 8, 8, 0)

    def set_block(self) -> None:
        """Set block at random
        """
        self.block = Block(
            shape=self.blocks.pop(random.randint(0, len(self.blocks) - 1))
                )

    def freeze_block(self) -> None:
        """Freezes the block to the grid
        """
        for tile in self.block.get_block_tiles(
            self.block.position, self.block.orientation
                ):
            self.grid[tile[0]][tile[1]] = 1
            self.grid_tile_colors[tile[0]][tile[1]] = self.block.shape

    def clear_rows(self) -> None:
        """Clear filled row
        """
        rows_to_clear = []
        for row in range(2, 34):
            if sum(self.grid[row]) == 10:
                rows_to_clear.append(row)
        if len(rows_to_clear) < 4:
            self.score += (100 * len(rows_to_clear))
        else:
            self.score += 800
        for row in rows_to_clear:
            for r in range(row, 1, -1):
                self.grid[r] = [x for x in self.grid[r - 1]]
                self.grid_tile_colors[r] = [x for x in self.grid_tile_colors[r - 1]]

    def change_score(self) -> None:
        """Change score and set flash timeout
        """
        self.score += 50
        self.score_color_timeout = 60

    def change_speed(self) -> None:
        """Change speed and set flash timeout
        """
        self.speed += 1
        self.speed_color_timeout = 60

    def set_color(self, color_attr: str) -> int:
        """Set flash color
        """
        val = getattr(self, color_attr)
        if val:
            setattr(self, color_attr, val - 1)
            return pyxel.frame_count % 8
        return 12

    def hide_reveal(self, marker: bool) -> int:
        """Hide or reveal flashed marker
        """
        if marker:
            return pyxel.frame_count % 8
        return 0

    def is_game_over(self) -> bool:
        """Check is game over
        """
        if self.block.position[0] == 0:
            return True
        return False
