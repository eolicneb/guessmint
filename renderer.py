from random import randint


class Renderer:
    def __init__(self, size):
        self.size = size
        self.legend = None

    def __call__(self, answer):
        dots, dot = set(), None
        for _ in range(answer):
            while not dot or dot in dots:
                dot = self._random_dot()
            dots.add(dot)
        self._show(dots)

    def _random_dot(self):
        I, J = self.size
        i = randint(0, I-1)
        j = randint(0, J-1)
        return (i, j)

    def _show(self, dots):
        I, J = self.size
        screen_ij = [["*" if (i, j) in dots else " " \
            for j in range(J)] for i in range(I)]
        screen = "\n".join(" ".join(line) for line in screen_ij)

        padding = "\n"*100
        if self.legend:
            padding += self.legend + "\n"
        print(padding + "\n" + screen)