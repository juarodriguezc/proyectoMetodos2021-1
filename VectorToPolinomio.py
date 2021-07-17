from sympy import *
lista = [-3, 4, 5, -6]
lista.append(-6)
def vtp(lista):
    x = Symbol('x')
    f_xS = ""
    for i in range(len(lista)):
        iS = str(lista[i])
        eS = str(len(lista) - i -1)
        nS = iS + "*x**" + eS
        if i == 0:
            f_xS = f_xS + nS
        else:
            f_xS = f_xS + " + " + nS
    polinomio = parse_expr(f_xS)
    return(polinomio)