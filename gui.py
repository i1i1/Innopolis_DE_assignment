import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, CheckButtons


class Gui:
    class _Numerical:
        def __init__(self, nm):
            self.nm = nm

        def add_graph(self, line, lerr, gerr):
            self.line = line
            self.lerr = lerr
            self.gerr = gerr

    def __init__(self, exact, x0, y0, X, h):
        self.exact = exact
        self.numericals = list()
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.h = h

        self.fig = plt.figure()

        gs = self.fig.add_gridspec(2, 5)
        self.ax_sol = self.fig.add_subplot(gs[:, :3], title='Solutions')
        self.ax_lerr = self.fig.add_subplot(gs[0, 3:], title='Local errors')
        self.ax_gerr = self.fig.add_subplot(gs[1, 3:], title='Global errors')

        self.ax_sol.grid(True)
        self.ax_lerr.grid(True)
        self.ax_gerr.grid(True)
        plt.subplots_adjust(left=0.2, bottom=0.2)

    def add_numericals(self, *numericals):
        for nu in numericals:
            self.numericals.append(Gui._Numerical(nu))

    def _add_checkbuttons(self):
        labels = [nu.nm.name for nu in self.numericals]
        visibility = [nu.line.get_visible() for nu in self.numericals]
        axes = plt.axes([0.05, 0.75, 0.10, 0.15], title='Plots')

        def checkbox_update(label):
            for nu in self.numericals:
                if nu.nm.name != label:
                    continue
                vis = not nu.line.get_visible()
                nu.line.set_visible(vis)
                nu.gerr.set_visible(vis)
                nu.lerr.set_visible(vis)
                self._redraw_plot()

        self.checkboxes = CheckButtons(axes, labels, visibility)
        self.checkboxes.on_clicked(checkbox_update)

    def show_window(self):
        n = max((self.X-self.x0) // self.h, 2)
        x = np.linspace(self.x0, self.X, n)
        ex = np.linspace(self.x0, self.X)

        self._lines = list()

        self.exact.set_constant(self.x0, self.y0)

        for nu in self.numericals:
            nm = nu.nm
            y = nm.get_y(x, self.y0)
            lerr = nm.get_lerr(x, self.y0, self.exact.exact)
            gerr = nm.get_gerr(x, self.y0, self.exact.exact)
            nu.add_graph(
                self.ax_sol.plot(x, y, "o-", label=nm.name)[0],
                self.ax_lerr.plot(x, lerr, "o-", label=nm.name)[0],
                self.ax_gerr.plot(x, gerr, "o-", label=nm.name)[0]
            )

        self._exact_line, = self.ax_sol.plot(ex, self.exact.exact(ex),
                                             label='exact')

        self._add_button("h",  [0.1, 0.1,   0.05, 0.05])
        self._add_button("x0", [0.2, 0.1,   0.05, 0.05])
        self._add_button("X",  [0.3, 0.1,   0.05, 0.05])
        self._add_button("y0", [0.2, 0.025, 0.05, 0.05])
        self._add_checkbuttons()
        self.ax_sol.legend()

        plt.show()

    def _replot(self):
        n = max((self.X-self.x0) // self.h, 2)
        x = np.linspace(self.x0, self.X, n)
        ex = np.linspace(self.x0, self.X)

        self.exact.set_constant(self.x0, self.y0)
        self._exact_line.set_data(ex, self.exact.exact(ex))

        for nu in self.numericals:
            x = np.linspace(self.x0, self.X, n)
            nu.line.set_data(x, nu.nm.get_y(x, self.y0))
            nu.lerr.set_data(x, nu.nm.get_lerr(x, self.y0, self.exact.exact))
            nu.gerr.set_data(x, nu.nm.get_gerr(x, self.y0, self.exact.exact))

        self._redraw_plot()

    def _redraw_plot(self):
        self.ax_sol.relim(visible_only=True)
        self.ax_sol.autoscale_view()
        self.ax_gerr.relim(visible_only=True)
        self.ax_gerr.autoscale_view()
        self.ax_lerr.relim(visible_only=True)
        self.ax_lerr.autoscale_view()
        plt.draw()

    def _add_button(self, var, box):
        def _callback(text):
            try:
                self.__setattr__(var, float(text))
                self._replot()
            except Exception as e:
                print(str(e))

        tb = TextBox(plt.axes(box), var+' = ',
                     initial=str(self.__getattribute__(var)))
        tb.on_submit(_callback)
        self.__setattr__('_tb_'+var, tb)
