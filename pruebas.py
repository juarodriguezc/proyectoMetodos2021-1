import matplotlib.pyplot as plt
import interpolinomial as pol
import interLagrange as lge
import intersplines as spl
import numpy as np
from sympy import *
from sympy.plotting import plot

#puntos = [[0, 1], [1, 3], [2, 0], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10]]

x = Symbol('x')
puntos = [[1, 2], [3, 3], [5, 5], [7, 3]]

polP = pol.polinomial(puntos)
lagP = lge.lagrange(puntos)
ecspl = spl.splines(puntos)
print(polP)
print(lagP)
print(ecspl)

p1 = plot(x**2, (x, -5, 5), x**3, (x, 5, 10))
p1.show