from random import randint
from time import time


class StatPoint:
    def __init__(self, answer):
        self.answer = answer
        self.guess = None
        self.time = time()

    def record(self, guess):
        self.time = time() - self.time
        self.guess = guess

    @property
    def difference(self):
        if self.guess is None:
            return None
        return self.guess - self.answer

    def __str__(self):
        return (f"correct: {self.answer:3d}"
                f" , guess: {self.guess:3d}"
                f"  (in {self.time:5.1f} sec.)")


class GuessCore:
    def __init__(self, cotas, renderer):

        self.cotas = cotas

        self.renderer = renderer

        self.times = 0
        self.goals = 0
        self.correct = False
        self.stats = []
        self.__stat_point = None

        self._answer = None
        self.lock = None

    @property
    def answer(self):
        if not self.lock:
            return self._answer

    def ruffle(self):
        self._answer = randint(*self.cotas)
        self.times += 1
        self.lock = True
        self.__stat_point = StatPoint(self._answer)

    def paint(self):
        self.renderer(self._answer)

    def check(self, guess):
        try:
            int_guess = int(guess)
        except ValueError:
            raise

        self.correct = (int_guess == self._answer)

        self.lock = False

        self.__stat_point.record(int_guess)
        self.stats.append(self.__stat_point)

        if self.correct:
            self.goals += 1

    @property
    def last_difference(self):
        if self.__stat_point is not None:
            return self.__stat_point.difference

    @property
    def result(self):
        return self.goals, self.times

    @property
    def std_dev(self):
        if self.times < 2:
            return 0
        return sum(x.difference*x.difference for x in self.stats) / (self.times - 1)
