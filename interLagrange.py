from sympy import *
def lagrange(puntos):
    x = Symbol('x')
    par = ""
    for i in range(len(puntos)):
        num = puntos[i][1]
        den = 1
        car = ""
        cont = 0
        for j in range(len(puntos)):
            if j != i:
                den = den * (puntos[i][0] - puntos[j][0])
                if cont == 0:
                    car = car + "(" + "x - " + str(puntos[j][0]) + ")"
                else:
                    car = car + "*" + "(" + "x - " + str(puntos[j][0]) + ")"
                cont = cont + 1
        coef = str(num) + "/" + str(den)

        if i == 0:
            par = par + coef + "*" + car
        else:
            par = par + " + " + coef + "*" + car
    polinomiont = parse_expr(par)
    polinomiot = expand(simplify(polinomiont))
    return polinomiot