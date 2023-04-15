import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Hello, world!")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(pyxel.frame_count % 8)
        pyxel.text(55, 41, "Hello, world!", 0)

        count = pyxel.frame_count
        while True:
            if count - 16 < 0:
                pyxel.text(55, 60, str(pyxel.colors[count]), 0)
                break
            else:
                count -= 16

App()