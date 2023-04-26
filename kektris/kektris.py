import pyxel
import random
from kektris.blocks import Grid, Figure, Window
from kektris.constraints import (
    Direction,
    FigureOrientation,
    ARRIVE,
        )


class Game:
    def __init__(self) -> None:
        pyxel.init(256, 256, title="Kektris")
        pyxel.load('blocks.pyxres', image=True)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self) -> None:
        """Reset game state
        """
        # Menyu parameters
        self.paused = True
        self.score = 0
        self.speed = 0
        self.score_color_timeout = 60
        self.speed_color_timeout = 60

        # grid
        self.grid: Grid = Grid()
        self.grid_higlight = False
        self.figure = self.arrive_figure()

    def draw(self) -> None:
        """Draw current screen
        """
        pyxel.cls(0)
        pyxel.rectb(10, 10, 205, 205, 1)

        pyxel.text(219, 20, "SCORE", 10)
        pyxel.text(219, 30, str(self.score), self._set_color("score_color_timeout"))

        pyxel.text(219, 50, "SPEED", 10)
        pyxel.text(219, 60, str(self.speed), self._set_color("speed_color_timeout"))

        pyxel.text(20, 226, "Q:quit", 8)

        pyxel.text(50, 226, "R:restart", 9)

        pyxel.text(88, 226, ">", self._hide_reveal(self.paused))
        pyxel.text(92, 226, "P:pause", 12)

        pyxel.text(122, 226, ">", self._hide_reveal(self.grid_higlight))
        pyxel.text(126, 226, "G:greed", 12)

        self.mark_grid()
        self.draw_figures()

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
        elif pyxel.btnp(pyxel.KEY_RIGHT, 12, 2):
            move_direction = Direction.RIGHT
        elif pyxel.btnp(pyxel.KEY_DOWN, 12, 2):
            move_direction = Direction.DOWN
        elif pyxel.btnp(pyxel.KEY_UP, 12, 2):
            move_direction = Direction.UP
        elif pyxel.btnp(pyxel.KEY_Z, 12, 20):
            rotate_direction = Direction.LEFT
        elif pyxel.btnp(pyxel.KEY_C, 12, 20):
            rotate_direction = Direction.RIGHT
        elif pyxel.btnp(pyxel.KEY_X, 12, 20):
            fall_center = True

        if move_direction:
            self.figure.move_figure(move_direction)
        if rotate_direction:
            self.figure.rotate_figure(rotate_direction)

        # FIXME: move random
        self.figure.move_figure(Direction.DOWN)

    def mark_grid(self) -> None:
        """Draw grid mark
        """
        if self.grid_higlight:
            for p in range(10, 217, 6):
                color = 13 if p != 112 else 15
                pyxel.line(p, 10, p, 214, color)
                pyxel.line(10, p, 214, p, color)

    def arrive_figure(self) -> Figure:
        """Arrive figure at random
        """
        top_left, orientation = self._generate_figure_start_position()
        window = Window(top_left, orientation, self.grid)
        return Figure(window)

    def _generate_figure_start_position(
        self) -> tuple[tuple[int, int], FigureOrientation]:
        """Genrate random start position
        """
        return (
            random.choice(ARRIVE),
            random.choice(FigureOrientation.get_includes())
                )

    def draw_figures(self) -> None:
        """Draw blocked and frozen from Grid object
        """
        for n, row in enumerate(self.grid.grid):
            for m, cell in enumerate(row):
                x = cell.pos[0] * 5 + 11 + n
                y = cell.pos[1] * 5 + 11 + m
                if cell.is_blocked:
                    pyxel.rect(x, y, 5, 5, 10)
                if cell.is_frozen:
                    pyxel.rect(x, y, 5, 5, 7)

    # TODO: rewrite this in Grid class
    def clear_rows(self) -> None:
        """Clear filled row
        """
        # rows_to_clear = []
        # for row in range(2, 34):
        #     if sum(self.grid[row]) == 10:
        #         rows_to_clear.append(row)
        # if len(rows_to_clear) < 4:
        #     self.score += (100 * len(rows_to_clear))
        # else:
        #     self.score += 800
        # for row in rows_to_clear:
        #     for r in range(row, 1, -1):
        #         self.grid[r] = [x for x in self.grid[r - 1]]
        #         self.grid_tile_colors[r] = [x for x in self.grid_tile_colors[r - 1]]


    # TODO: check is need to freeze (move to grid)

    # TODO: check is need to clear (move to grid)

    def _change_score(self) -> None:
        """Change score and set flash timeout
        """
        self.score += 50
        self.score_color_timeout = 60

    def _change_speed(self) -> None:
        """Change speed and set flash timeout
        """
        self.speed += 1
        self.speed_color_timeout = 60

    def _set_color(self, color_attr: str) -> int:
        """Set flash color
        """
        val = getattr(self, color_attr)
        if val:
            setattr(self, color_attr, val - 1)
            return pyxel.frame_count % 8
        return 12

    def _hide_reveal(self, marker: bool) -> int:
        """Hide or reveal flashed marker
        """
        if marker:
            return pyxel.frame_count % 8
        return 0

    def _is_game_over(self) -> bool:
        """Check is game over
        """
        # if self.block.position[0] == 0:
        #     return True
        # return False
