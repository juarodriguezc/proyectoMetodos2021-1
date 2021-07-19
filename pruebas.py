import matplotlib.pyplot as plt
import interpolinomial as pol
import interLagrange as lge
from sympy import *

puntos = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10]]
polP = pol.polinomial(puntos)
lagP = lge.lagrange(puntos)
print(polP)
print(lagP)
#plot(polP)
plot(lagP)
