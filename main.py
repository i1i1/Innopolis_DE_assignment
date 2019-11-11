#!/usr/bin/python3
from gui import Gui
from numerical import ExactAbstract, EulerMethod, \
    ImprovedEulerMethod, RungeKuttaMethod
import math as m


class Exact(ExactAbstract):
    def derivative(x, y):
        return (1 + y/x) * m.log(1 + y/x) + y/x

    def exact(self, x):
        return (m.e ** (self.c * x) - 1) * x

    def set_constant(self, x0, y0):
        self.c = m.log(y0/x0 + 1) / x0


x0, y0, X, h = 1, 2, 6, 0.5

g = Gui(Exact(), x0, y0, X, h)
g.add_numericals(EulerMethod(Exact.derivative),
                 ImprovedEulerMethod(Exact.derivative),
                 RungeKuttaMethod(Exact.derivative))
g.show_window()
