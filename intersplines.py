import interLagrange as lag
import VectorToPolinomio as VTP
import numpy as np
from numpy import *
from scipy import *
from sympy import *
def splines(puntos):
    x = Symbol('x')
    longitud = len(puntos)
    coeficientes = []
    solucion = [[puntos[0][1]]]
    for i in range(2 * (longitud - 1)):
        cf = []
        if i % 2 == 0:
            numero = puntos[int(i/2)][0]
        else:
            numero = puntos[int(i/2) + 1][0]

        for j in range(int(i/2) * 4):
            cf.append(0)

        cf.append(numero ** 3)
        cf.append(numero ** 2)
        cf.append(numero)
        cf.append(1)
        for j in range(((longitud - 1) * 4) - int(i/2) * 4 - 4):
            cf.append(0)
        coeficientes.append(cf)
    for i in range(longitud - 2):
        cfd = []
        punto = puntos[i + 1][0]
        for j in range(i * 4):
            cfd.append(0)
        cfd.append(3 * (punto ** 2))
        cfd.append(2 * punto)
        cfd.append(1)
        cfd.append(0)
        cfd.append(-3 * (punto ** 2))
        cfd.append(-2 * (punto))
        cfd.append(-1)
        cfd.append(0)
        for j in range(4 * (longitud - 1) - (8 + i * 4)):
            cfd.append(0)
        coeficientes.append(cfd)
    for i in range(longitud - 2):
        cfdd = []
        punto = puntos[i + 1][0]
        for j in range(i * 4):
            cfdd.append(0)
        cfdd.append(6 * punto)
        cfdd.append(2)
        cfdd.append(0)
        cfdd.append(0)
        cfdd.append(-6 * punto)
        cfdd.append(-2)
        cfdd.append(0)
        cfdd.append(0)
        for j in range(4 * (longitud - 1) - (8 + i * 4)):
            cfdd.append(0)
        coeficientes.append(cfdd)

    ext0 = [3 * (puntos[0][0] ** 2), 2 * puntos[0][0], 1, 0]
    for i in range(4 * (longitud - 1) - 4):
        ext0.append(0)
    coeficientes.append(ext0)
    ext1 = []
    for i in range(4 * (longitud - 1) - 4):
        ext1.append(0)
    ext1.append(3 * (puntos[longitud - 1][0] ** 2))
    ext1.append(2 * puntos[longitud - 1][0])
    ext1.append(1)
    ext1.append(0)
    coeficientes.append(ext1)

    for i in range(1, longitud - 1):
        solucion.append([puntos[i][1]])
        solucion.append([puntos[i][1]])
    solucion.append([puntos[longitud - 1][1]])
    for i in range(longitud - 2):
        solucion.append([0])
        solucion.append([0])
    polinomio = lag.lagrange(puntos)
    derivado = diff(polinomio, x)
    p0 = derivado.evalf(subs = {x:puntos[0][0]})
    p1 = derivado.evalf(subs = {x:puntos[longitud - 1][0]})

    solucion.append([float(round(p0, 5))])
    solucion.append([float(round(p1, 5))])

    r = linalg.solve(coeficientes, solucion)
    rarray = []
    for i in range(len(r)):
        rarray.append(round(r[i][0], 5))

    ecuaciones = []

    for i in range(longitud - 1):
        y=np.linspace(puntos[i][0], puntos[i + 1][0])
        ecuaciones.append(VTP.vtp([rarray[i * 4], rarray[i * 4 + 1], rarray[i * 4 + 2], rarray[i * 4 + 3]]))

    return ecuaciones