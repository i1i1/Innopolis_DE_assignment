import numpy as np
from abc import ABC, abstractmethod


class ExactAbstract(ABC):
    @abstractmethod
    def derivative(x, y):
        pass

    @abstractmethod
    def exact(self, x):
        pass

    @abstractmethod
    def set_constant(self, x0, y0):
        pass


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
        for i in x[:-1]:
            y.append(self._next(h, i, y[-1]))
        return y

    def get_lerr(self, x0, y0, X, h, exact):
        n = max(int((X-x0) // h), 2)
        x = np.linspace(x0, X, n)
        lerr = list()
        for i in range(1, n):
            y_num = self._next(h, x[i-1], exact(x[i-1]))
            y_exact = exact(x[i])
            lerr.append(abs(y_exact - y_num))
        return range(1, n), lerr

    def get_gerr(self, x0, y0, X, h, exact):
        n = max(int((X-x0) // h), 2)
        gerr = list()
        for i in range(2, n+1):
            x = np.linspace(x0, X, i)
            num = self.get_y(x, y0)
            ex = exact(x)
            gerr.append(abs(ex-num)[-1])
        return range(1, n), gerr


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
