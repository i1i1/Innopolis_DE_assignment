#!/usr/bin/python3
from gui import Gui
from numerical import *


class Exact(ExactAbstract):
    def derivative(x, y):
        return (1 + y/x) * log(1 + y/x) + y/x

    def _partial(self, x):
        return (3 ** x - 1) * x


x0, y0, X, h = 1, 2, 6, 0.5

g = Gui(Exact(), x0, y0, X, h)
g.add_numericals(EulerMethod(Exact.derivative),
                 ImprovedEulerMethod(Exact.derivative),
                 RungeKuttaMethod(Exact.derivative))
g.show_window()
