from numpy import log
from abc import ABC, abstractmethod


class ExactAbstract(ABC):
    @abstractmethod
    def derivative(x, y):
        pass

    @abstractmethod
    def _partial(self, x):
        pass

    def exact(self, x):
        return self._partial(x) + self.c

    def set_constant(self, x, y):
        self.c = y - self._partial(x)


class NumericalMethod(ABC):
    name = "Name of numerical method"

    def __init__(self, der):
        self.der = der

    @abstractmethod
    def _next(self, h, x0, y0):
        pass

    def get_y(self, x, y0):
        y = [y0]
        h = x[1] - x[0]
        for i in range(1, len(x)):
            y.append(self._next(h, x[i-1], y[i-1]))
        return y


class EulerMethod(NumericalMethod):
    name = "Euler"

    def _next(self, h, x0, y0):
        return y0 + h * self.der(x0, y0)


class ImprovedEulerMethod(NumericalMethod):
    name = "Improved Euler"

    def _next(self, h, x0, y0):
        k1 = self.der(x0, y0)
        k2 = self.der(x0 + h, y0 + h*k1)
        return y0 + h * (k1 + k2) / 2


class RungeKuttaMethod(NumericalMethod):
    name = "Runge-Kutta"

    def _next(self, h, x0, y0):
        k1 = self.der(x0,       y0)
        k2 = self.der(x0 + h/2, y0 + h*k1/2)
        k3 = self.der(x0 + h/2, y0 + h*k2/2)
        k4 = self.der(x0 + h,   y0 + h*k3)
        return y0 + h * (k1 + 2*k2 + 2*k3 + k4) / 6
