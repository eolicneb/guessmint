from __future__ import annotations

from tkinter import (Tk, Text, StringVar, DoubleVar, Canvas,
                     RIGHT, BOTH, BOTTOM, SUNKEN, TOP, LEFT, END, X)
from tkinter.ttk import Frame, Button, Label, Style

from random_grid import RandomGrid
from guess_core import GuessCore


class GuessGui(Frame):
    button_labels = ("NEW", "GO")
    guess_box_initial = ""
    diff_color = {
        'negative': "magenta",
        'just': "green",
        'positive': "cyan"
    }

    def __init__(self, root: Tk, cotas):
        super().__init__(root)

        self.guess_core = GuessCore(cotas, self)

        self.marquesine = StringVar(value="Results:")

        self.initUI()
        self.pack(fill=BOTH, expand=True)

    def initUI(self):
        self.master.title("GuessMint")
        self.style = Style()
        self.style.theme_use("default")

        self.friso = Label(self, textvariable=self.marquesine)
        self.friso.pack(side=TOP, padx=5, pady=5)

        frame = Frame(self, relief=SUNKEN, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.projector = GraphGrid(frame)
        self.projector.pack(fill=BOTH, pady=10, padx=10, expand=True)

        bottom = Frame(self)
        bottom.pack(side=BOTTOM, fill=X)

        self.ok_button = Button(bottom, text="GO", command=self._action_ok)
        self.ok_button.pack(side=RIGHT, pady=5, padx=5, fill=BOTH)

        self.guess_box = Text(bottom, width=4, height=1)
        self.guess_box.bind("<KeyPress>", self.enter_callback)
        self.guess_box.insert("1.0", self.guess_box_initial)
        self.guess_box.pack(side=LEFT, pady=5, padx=5, expand=False)

        self.index_display = Index(bottom)
        self.index_display.pack(side=RIGHT, pady=5, padx=5, expand=False)
        self.index_display.redraw()

    def project(self, count):
        self.projector.project(count)

    def _action_ok(self):
        if self.guess_core.lock:
            self.check_guess()
        else:
            self.new_riddle()

    @property
    def guess_value(self):
        return self.guess_box.get("1.0", END)

    def reset_guess_value(self):
        self.guess_box.delete("1.0", END)
        self.guess_box.focus()

    def check_guess(self):
        try:
            self.guess_core.check(self.guess_value)
            self.show_difference()
            self.ok_button.configure(text=self.button_labels[0])
        except ValueError:
            self.reset_guess_value()

    def show_difference(self):
        diff = self.guess_core.last_difference
        diff_sign = 'positive' if diff > 0 else 'negative' if diff < 0 else 'just'
        self.projector.write(self.guess_core.last_difference,
                             color=self.diff_color[diff_sign])

    def new_riddle(self):
        self.renew_marquesine()
        self.renew_index_display()
        self.projector.erase()
        self.guess_core.ruffle()
        self.guess_core.paint()
        self.ok_button.configure(text=self.button_labels[1])
        self.reset_guess_value()

    def renew_marquesine(self):
        goals, tests = self.guess_core.result
        self.marquesine.set(f"Results: {goals} / {tests}")

    def renew_index_display(self):
        self.index_display.set(self.guess_core.std_dev)
        self.index_display.redraw()

    def __call__(self, guess_value):
        self.projector.project(guess_value)

    def enter_callback(self, event):
        if event.keysym == "Return":
            self.ok_button.invoke()


class GraphGrid(Canvas):
    text_color = "cyan"

    def __init__(self, root, ball_radius=10):
        super().__init__(root)
        self.radius = ball_radius
        self.compress = ball_radius * 0.7
        self.balls = []
        self.init_canvas()
        self.text = None

    def init_canvas(self):
        self.style = Style()
        self.style.theme_use("default")
        self.configure(bg="black")
        self.pack(fill=BOTH, expand=True)

    def project(self, count):
        for ball in self.balls:
            self.delete(ball)
        for pos in self.get_random(count):
            self.put_ball(*pos)

    def write(self, text, color=None):
        w, h = (x // 2 for x in self.size)
        color = self.text_color if color is None else color
        self.text = self.create_text((w, h), text=text, fill=color,
                                     font=self.text_font_tuple())

    @staticmethod
    def text_font_tuple(font="roboto", size=24, style="bold"):
        return font, size, style

    def erase(self):
        if self.text is not None:
            self.delete(self.text)
            self.text = None

    @property
    def size(self):
        return self.winfo_width(), self.winfo_height()

    @property
    def random_grid(self):
        grid_w, grid_h = self.size
        grid_w -= self.radius * 2
        grid_h -= self.radius * 2
        grid_w //= self.radius * 2
        grid_h //= self.radius * 2
        return RandomGrid((grid_w, grid_h))

    def get_random(self, count):
        for i, j in self.random_grid.get(count):
            yield self.radius * (2*i + 2), self.radius * (2*j + 2)

    def put_ball(self, x, y, color="yellow"):
        x0, x1 = x - self.compress, x + self.compress
        y0, y1 = y - self.compress, y + self.compress
        self.balls.append(self.create_oval(x0, y0, x1, y1, fill=color, outline=''))


class Index(Canvas):
    def __init__(self, root, unit_px=10, width_units=3,
                 bg_color="grey", base_color="black", main_color="white"):
        super().__init__(root)

        self.unit_px = unit_px
        self.width_units = width_units

        self.bg_color = bg_color
        self.base_color = base_color
        self.main_color = main_color

        self.value = DoubleVar()

        self.init_ui()
        self.redraw()

    def init_ui(self):
        self.configure(width=2*self.unit_px*self.width_units, height=25,
                       bg=self.bg_color)

        self.value.set(0.5)
        self.draw()

    def draw(self):
        self.value_index = self.create_oval(0, 0, 0, 0, fill=self.main_color)
        self.base_line = self.create_line(0, 0, 0, 0, fill=self.base_color)
        self.zero_index = self.create_line(0, 0, 0, 0, fill=self.base_color)
        self.ticks = [self.create_line(*p, fill=self.base_color) for p in self.make_ticks()]

    def redraw(self):
        width, height = self.size
        half_height = height // 2
        self.coords(self.base_line, 0, half_height, width, half_height)
        self.coords(self.zero_index, *self.center_pos)
        self.coords(self.value_index, *self.index_pos(self.value.get()))
        for tick, pos in zip(self.ticks, self.make_ticks()):
            self.coords(tick, *pos)

    def set(self, value):
        self.value.set(value)
        self.redraw()

    @property
    def center_pos(self):
        w, h = self.size
        c = w // 2
        return c, 0, c, h

    def index_pos(self, value: float):
        x0, y0, x1, y1 = self.center_pos
        x_pos_right = int(value * self.unit_px) + x0
        x_pos_left = - int(value * self.unit_px) + x0
        return x_pos_left, y0, x_pos_right, y1

    def tick_pos(self, unit: int):
        xc, _, _, h = self.center_pos
        x = xc + self.unit_px * unit
        y0, y1 = h // 4, (3*h) // 4
        return x, y0, x, y1

    def make_ticks(self):
        for i in range(1-self.width_units, self.width_units):
            if not i:
                continue
            yield self.tick_pos(i)

    @property
    def size(self):
        print(f"W={self.winfo_width()}, H={self.winfo_height()}")
        return self.winfo_width(), self.winfo_height()


def gui_main():
    root = Tk()
    root.geometry("600x650")
    app = GuessGui(root, (6, 12))
    root.mainloop()


if __name__ == "__main__":
    gui_main()
