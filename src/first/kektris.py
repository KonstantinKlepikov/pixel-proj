import pyxel


class App:
    def __init__(self) -> None:
        pyxel.init(256, 256, title="Kektris")
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self) -> None:
        self.paused = True
        self.score = 0
        self.speed = 0
        self.score_color_timout = 60
        self.speed_color_timeout = 60

    def update(self) -> None:
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

    def draw(self) -> None:
        pyxel.rectb(10, 10, 206, 206, 1)

        pyxel.text(220, 20, "SCORE", 10)
        pyxel.text(220, 30, str(self.score), self.set_color("score_color_timout"))

        pyxel.text(220, 50, "SPEED", 10)
        pyxel.text(220, 60, str(self.speed), self.set_color("speed_color_timeout"))

        pyxel.text(20, 226, "Q:quit", 8)
        pyxel.text(50, 226, "R:restart", 9)
        pyxel.text(92, 226, "P:pause", 12)
        pyxel.text(100, 236, 'paused', self.set_paused_color())

    def change_score(self) -> None:
        self.score += 50
        self.speed_color_timeout = 60

    def change_speed(self) -> None:
        self.speed += 1
        self.speed_color_timeout = 60

    def set_color(self, color_attr: str) -> int:
        val = getattr(self, color_attr)
        if val:
            setattr(self, color_attr, val - 1)
            return pyxel.frame_count % 8
        return 12

    def set_paused_color(self) -> int:
        if self.paused:
            return pyxel.frame_count % 8
        return 0


App()
