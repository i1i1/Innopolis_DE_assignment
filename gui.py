import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox


class Gui:
    title = "numerical method comparison"

    def __init__(self, exact, x0, y0, X, h):
        self.exact = exact
        self.numericals = []
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.h = h

        self.fig, self.ax = plt.subplots()

        self.ax.relim()
        self.ax.autoscale_view()

        self.ax.set_title(self.title)
        self.ax.legend()
        self.ax.grid(True)


    def add_numericals(self, *numericals):
        self.numericals += [*numericals]

    def show_window(self):
        plt.subplots_adjust(bottom=0.2)

        n = max((self.X-self.x0) // self.h, 2)
        x = np.linspace(self.x0, self.X, n)
        ex = np.linspace(self.x0, self.X)

        self._lines = []

        for nm in self.numericals:
            line, = self.ax.plot(x, nm.get_y(x, self.y0), "o-", label=nm.name)
            self._lines.append(line)

        self._exact_line, = self.ax.plot(ex, self.exact(ex), label='exact')

        self._add_button("h",  [0.1, 0.1,   0.05, 0.05])
        self._add_button("x0", [0.2, 0.1,   0.05, 0.05])
        self._add_button("X",  [0.3, 0.1,   0.05, 0.05])
        self._add_button("y0", [0.2, 0.025, 0.05, 0.05])

        plt.show()

    def _replot(self):
        n = max((self.X-self.x0) // self.h, 2)
        x = np.linspace(self.x0, self.X, n)
        ex = np.linspace(self.x0, self.X)

        for i in range(len(self.numericals)):
            line = self._lines[i]
            nm = self.numericals[i]

            line.set_data(x, nm.get_y(x, self.y0))

        self._exact_line.set_data(ex, self.exact(ex))

        plt.draw()

    def _add_button(self, var, box):
        def _callback(text):
            try:
                self.__setattr__(var, float(text))
                self._replot()
            except exception as e:
                print(str(e))

        tb = TextBox(plt.axes(box), var+' = ',
                     initial=str(self.__getattribute__(var)))
        tb.on_submit(_callback)
        self.__setattr__('_tb_'+var, tb)
