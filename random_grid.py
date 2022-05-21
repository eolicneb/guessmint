from random import randint


class RandomGrid:
    def __init__(self, size):
        self.w, self.h = size

    def _random_dot(self):
        i = randint(0, self.w-1)
        j = randint(0, self.h-1)
        return i, j

    def get(self, count) -> set:
        dots, dot = set(), None
        for _ in range(count):
            while not dot or dot in dots:
                dot = self._random_dot()
            dots.add(dot)
        return dots
