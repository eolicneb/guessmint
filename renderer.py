from random_grid import RandomGrid


class Renderer:
    def __init__(self, size):
        self.grid = RandomGrid(size)
        self.legend = None
        self.padding = "\n"*100

    def __call__(self, answer):
        self._show(answer)

    def screen(self, count):
        screen_ij = [["*" if (i, j) in self.grid.get(count) else " "
                      for j in range(self.grid.h)] for i in range(self.grid.w)]
        return "\n".join(" ".join(line) for line in screen_ij)

    def _show(self, answer):
        padding = self.padding
        if self.legend:
            padding += self.legend + "\n"
        print(padding + "\n" + self.screen(answer))
