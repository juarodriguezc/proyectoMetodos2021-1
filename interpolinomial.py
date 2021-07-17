from numpy import *
from scipy import *
#puntos = [[0, 1], [1, 2], [2, 3]]
puntos = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10]]
def polinomial(puntos):
    longitud = len(puntos)
    coeficientes = []
    solucion = []
    for i in range(longitud):
        coeficientes.append([])
        for j in range(longitud):
            coeficientes[i].append(puntos[i][0] ** ((longitud - j) - 1))
    for i in range(longitud):
        solucion.append([])
        solucion[i].append(puntos[i][1])

    r = linalg.solve(coeficientes, solucion)
    rarray = []

    for i in range(len(r)):
        rarray.append(round(r[i][0], 5))
    return(rarray)