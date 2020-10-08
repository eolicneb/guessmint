from guess_core import GuessCore
from renderer import Renderer


def test_run(test, renderer):

    corrects, tries = test.result
    renderer.legend = f"{corrects} correct out of {tries}"

    test.ruffle()
    test.paint()
    guess = input("\nHow many * are there? ")

    test.check(guess)
    if test.correct:
        input(f"Right!")
    else:
        input(f"Nope, there were {test.answer}.")


if __name__ == "__main__":

    renderer = Renderer((10, 20))
    test = GuessCore((4, 10), renderer)

    while True:
        try:
            test_run(test, renderer)
        except ValueError:
            break

    print("\nRecord:")
    for point in test.stats:
        print("  ", point)