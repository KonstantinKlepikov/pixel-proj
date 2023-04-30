import pyxel
import random
from typing import Optional
from kektris.blocks import Grid, Figure, Window, Cell
from kektris.constraints import (
    Direction,
    FigureOrientation,
    ARRIVE,
    LEFT_QUARTER,
    RIGHT_QUARTER,
    TOP_QUARTER,
    BOTTOM_QUARTER,
        )


class Game:
    def __init__(self) -> None:
        pyxel.init(256, 256, title="Kektris")
        # pyxel.load('blocks.pyxres', image=True)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self) -> None:
        """Reset game state
        """
        # menu parameters
        self.paused = True
        self.score = 0
        self.speed = 0  # TODO: add speed grown logic
        self.score_color_timeout = 60
        self.speed_color_timeout = 60

        # grid
        self.grid: Grid = Grid()
        self.grid_higlight = False
        self.figure = self._arrive_figure()

        # game
        self.frame_count_from_last_move = 0
        self.clear_lenght = 8

    def draw(self) -> None:
        """Draw current screen
        """
        pyxel.cls(0)
        self._draw_controls()
        self._draw_aside()
        self._mark_grid()
        self._draw_figures()

    def update(self) -> None:
        """Update current game state
        """
        if pyxel.btnp(pyxel.KEY_T):
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

        if self.figure.is_ready_for_freeze_figure():
            self.grid.freeze_blocked()
            self.figure = self._arrive_figure()

        move_direction = None
        rotate_direction = None
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
        elif pyxel.btnp(pyxel.KEY_X, 12, 20):
            rotate_direction = Direction.RIGHT

        if move_direction:
            window = self.figure.move_figure(move_direction)
            if self.figure.is_valid_figure(window):
                self.figure.block_figure(window)
                self.figure.set_cells_move_direction()

        if rotate_direction:
            window = self.figure.rotate_figure(rotate_direction)
            if self.figure.is_valid_figure(window):
                self.figure.block_figure(window)
                self.figure.set_cells_move_direction()

        if self.frame_count_from_last_move == 45 - self.speed:
            window = self.figure.move_figure(self.figure.window.move_direction)
            if self.figure.is_valid_figure(window):
                self.figure.block_figure(window)
                self.figure.set_cells_move_direction()
            else:
                self.grid.freeze_blocked()
                self.figure = self._arrive_figure()

            self.frame_count_from_last_move = 0
            return

        self._clear_rows()

        # check is game end and stop iteration

        self.frame_count_from_last_move += 1

    def _draw_controls(self) -> None:
        """Draw controls
        """
        pyxel.rectb(14, 220, 13, 13, 1)
        pyxel.rectb(28, 220, 13, 13, 12)
        pyxel.rectb(42, 220, 13, 13, 1)
        pyxel.rectb(14, 235, 13, 13, 12)
        pyxel.rectb(28, 235, 13, 13, 12)
        pyxel.rectb(42, 235, 13, 13, 12)

        pyxel.text(19, 224, "Z", 1)
        pyxel.text(33, 223, "^", 12)
        pyxel.text(47, 224, "W", 1)
        pyxel.text(19, 239, "<", 12)
        pyxel.text(33, 239, "v", 12)
        pyxel.text(47, 239, ">", 12)

        pyxel.rectb(62, 220, 13, 13, 8)
        pyxel.text(67, 224, "T", 8)
        pyxel.text(77, 224, "exit", 8)

        pyxel.rectb(95, 220, 13, 13, 9)
        pyxel.text(100, 224, "R", 9)
        pyxel.text(110, 224, "restart", 9)

        pyxel.rectb(140, 220, 13, 13, 12)
        pyxel.text(145, 224, "P", self._hide_reveal(self.paused))
        pyxel.text(155, 224, "pause", 12)

        pyxel.rectb(177, 220, 13, 13, 12)
        pyxel.text(182, 224, "G", self._hide_reveal(self.grid_higlight))
        pyxel.text(192, 224, "greed", 12)

    def _draw_aside(self) -> None:
        """Draw aside parameters
        """
        pyxel.text(219, 20, "SCORE", 10)
        pyxel.text(219, 30, str(self.score), self._set_color("score_color_timeout"))

        pyxel.text(219, 50, "SPEED", 10)
        pyxel.text(219, 60, str(self.speed), self._set_color("speed_color_timeout"))

        pyxel.text(219, 80, "LINE", 10)
        pyxel.text(219, 90, str(self.clear_lenght), 12)

    def _mark_grid(self) -> None:
        """Draw grid mark
        """
        match self.figure.window.move_direction:
            case Direction.RIGHT | Direction.LEFT:
                color = (15, pyxel.frame_count % 8)
            case Direction.DOWN | Direction.UP:
                color = (pyxel.frame_count % 8, 15)
            case _:
                color = (15, 15)
        pyxel.line(112, 10, 112, 214, color[1])
        pyxel.line(10, 112, 214, 112, color[0])

        if self.grid_higlight:
            for p in range(10, 217, 6):
                if p != 112:
                    pyxel.line(p, 10, p, 214, 13)
                    pyxel.line(10, p, 214, p, 13)

        pyxel.rectb(10, 10, 205, 205, 1)

    def _arrive_figure(self) -> Figure:
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

    def _draw_figures(self) -> None:
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

    def _get_chunked(
        self,
        line: list[int],
        chunked: list[list[int]]
            ) -> tuple[list, list[list[int]]]:
        """Separate line to chunked lines
        """
        chunk = []
        while line:
            a = line.pop()
            if chunk:
                if chunk[-1] - a == 1:
                    chunk.append(a)
                else:
                    line.append(a)
                    line, chunked = self._get_chunked(line, chunked)
            else:
                chunk.append(a)
        chunked.append(chunk)
        return line, chunked

    def _check_line(
        self,
        dimension: int,
        frozen_pos: list[tuple[int, int]]
        ) -> Optional[list[tuple[int, int]]]:
        """Check is line ready to clear
        """
        s_d = 0 if dimension else 1
        comparison = [c[dimension] for c in frozen_pos]
        min_ = min(comparison)
        max_ = max(comparison) + 1
        for n in range(min_, max_):
            line = [pos for pos in frozen_pos if pos[dimension] == n]
            if len(line) >= self.clear_lenght:
                l_comparison = sorted([pos[s_d] for pos in line])
                _, chunked = self._get_chunked(l_comparison, [])
                to_clear = [
                    n for chunk in chunked
                    for n in chunk
                    if len(chunk) >= self.clear_lenght
                        ]
                if to_clear:
                    return [pos for pos in line if pos[s_d] in to_clear]

    def _move_frozen(self, frozen_to_move: list[Cell]) -> None:
        """Move frozen rows after clear
        """
        match self.figure.window.move_direction:
            case Direction.RIGHT:
                candidates = [self.grid.grid[cell.x+1][cell.y] for cell in frozen_to_move]
                quarter = LEFT_QUARTER
            case Direction.LEFT:
                candidates = [self.grid.grid[cell.x-1][cell.y] for cell in frozen_to_move]
                quarter = RIGHT_QUARTER
            case Direction.UP:
                candidates = [self.grid.grid[cell.x][cell.y-1] for cell in frozen_to_move]
                quarter = BOTTOM_QUARTER
            case Direction.DOWN:
                candidates = [self.grid.grid[cell.x][cell.y+1] for cell in frozen_to_move]
                quarter = TOP_QUARTER
        count = 0
        for new_, old in zip(candidates, frozen_to_move):
            if not new_.is_frozen and new_.pos in quarter:
                old.clear()
                new_.freeze()
                new_.move_direction = self.figure.window.move_direction
                count += 1
        if count:
            frozen_to_move = [
                cell for cell
                in self.grid.get_frozen
                if cell.move_direction == self.figure.window.move_direction
                    ]
            self._move_frozen(frozen_to_move)

    def _clear_rows(self) -> None:
        """Clear filled row
        """
        frozen = self.grid.get_frozen
        if len(frozen) >= self.clear_lenght:
            frozen_pos = [cell.pos for cell in frozen]
            for dim in [0, 1]:
                line = self._check_line(dim, frozen_pos)
                if line:
                    for pos in line:
                        self.grid.grid[pos[0]][pos[1]].clear()
                    self._clear_rows()
                    frozen_to_move = [
                        cell for cell
                        in self.grid.get_frozen
                        if cell.move_direction == self.figure.window.move_direction
                            ]
                    self._move_frozen(frozen_to_move)

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
        return 12

    def _is_game_over(self) -> bool:
        """Check is game over
        """
        # if self.block.position[0] == 0:
        #     return True
        # return False
