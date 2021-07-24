import matplotlib.pyplot as plt
import interpolinomial as pol
import interLagrange as lge
import intersplines as spl
import numpy as np
from sympy import *
#puntos = [[0, 1], [1, 3], [2, 0], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10]]

x = Symbol('x')
puntos = [(-1, 5), (-0.850187265917603, 4.4878892733564015), (-0.02621722846441943, 2.093425605536332), (0.797752808988764, 1.055363321799308), (1, 1), (1.6217228464419478, 1.3667820069204153), (2.445692883895131, 3.0346020761245676)]

polP = pol.polinomial(puntos)
lagP = lge.lagrange(puntos)
ecspl = spl.splines(puntos)
print(polP)
print(lagP)
print(ecspl)
x1 = np.linspace(puntos[0][0], puntos[len(puntos) - 1][0], num = 100)
fnp = lambdify(x, polP, 'numpy')
fnl = lambdify(x, lagP, 'numpy')
plt.plot(x1, fnp(x1), color = "r", label = "Polinomial:" + str(polP).replace("**", "^"))
plt.plot(x1, fnl(x1), color = "b", label = "Lagrange:" + str(lagP).replace("**", "^"))
for i in range(len(ecspl)):
    x2 = np.linspace(puntos[i][0], puntos[i + 1][0], num = 100)
    fnt = lambdify(x, ecspl[i], 'numpy')
    if i == 0:
        plt.plot(x2, fnt(x2), color = "g", label = "Splines")
    else:
        plt.plot(x2, fnt(x2), color = "g")
#plt.legend()
plt.show()