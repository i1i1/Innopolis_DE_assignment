#!/usr/bin/python3
from gui import Gui
from numerical import *


x0, y0, X, h = 1, 2, 6, 0.5

g = Gui(Exact.exact, x0, y0, X, h)
g.add_numericals(EulerMethod(Exact.derivative),
                 ImprovedEulerMethod(Exact.derivative),
                 RungeKuttaMethod(Exact.derivative))
g.show_window()
