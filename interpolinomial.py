from numpy import *
from scipy import *
import VectorToPolinomio as VTP
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
    return(VTP.vtp(rarray))


    