import pyxel


class App:
    def __init__(self):
        pyxel.init(256, 256, title="Kektris")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.rectb(10, 10, 206, 206, 1)

        pyxel.text(220, 20, "SCORE: ", 10)
        pyxel.text(220, 30, 'here is', 12)  # TODO: add score and flash
        pyxel.text(220, 50, "SPEED: ", 10)
        pyxel.text(220, 60, 'here is', 12)  # TODO: add current speed and flash

        pyxel.text(20, 226, "Q:quit", 8)
        pyxel.text(60, 226, "P:pause", 9)
        pyxel.text(100, 226, "R:restart", 11)

App()
