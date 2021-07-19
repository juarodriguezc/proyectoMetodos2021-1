import matplotlib.pyplot as plt
import interpolinomial as pol
import VectorToPolinomio as VTP
import interLagrange as lge
from sympy import *

puntos = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10]]
#polV = pol.polinomial(puntos)
#polP = VTP.vtp(polV)
lagP = lge.lagrange(puntos)
#print(lagP)
#print(polP)
print(lagP)
plot(lagP)