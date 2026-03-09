#%% Libraries
from sympy import Eq, sympify, simplify, pretty, symbols
import time
import sys

#%% Equations
'''Las ecuaciones se guardan en una matriz, cada fila corresponde a un nivel, desde el nivel 0 (tutorial) hasta el 5'''
x = symbols('x')

ecuaciones = [
    Eq(x + 8, 10),
    Eq(x - 5, 2),
    Eq(4*x, 12),
    Eq(x/5 - 4, 0),
    Eq(5*x - 40, 2*x + 38)
]

#%% Functions

def escribir_lento(texto, velocidad=0.07, pausa_final=1):
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(velocidad)
    print()
    time.sleep(pausa_final)

def bloque(expr):
    """Devuelve el bloque de texto de una expresión."""
    lineas = pretty(expr).split("\n")
    ancho = max(len(l) for l in lineas)
    lineas = [l.center(ancho) for l in lineas]
    return lineas, ancho

def igualar_alturas(lhs_lines, rhs_lines, lhs_w, rhs_w):

    h = max(len(lhs_lines), len(rhs_lines))

    lhs_pad = (h - len(lhs_lines)) // 2
    rhs_pad = (h - len(rhs_lines)) // 2

    lhs_lines = ([" " * lhs_w] * lhs_pad +
                 lhs_lines +
                 [" " * lhs_w] * (h - len(lhs_lines) - lhs_pad))

    rhs_lines = ([" " * rhs_w] * rhs_pad +
                 rhs_lines +
                 [" " * rhs_w] * (h - len(rhs_lines) - rhs_pad))

    return lhs_lines, rhs_lines

def mostrar_vertical(eq, operador=None, expr=None):

    lhs_lines, lhs_w = bloque(eq.lhs)
    rhs_lines, rhs_w = bloque(eq.rhs)

    lhs_lines, rhs_lines = igualar_alturas(lhs_lines, rhs_lines, lhs_w, rhs_w)

    for l, r in zip(lhs_lines, rhs_lines):
        print(l + " = " + r)

    if operador is None:
        return

    op = f"{operador}{expr}"

    op_l = op.center(lhs_w)
    op_r = op.center(rhs_w)

    print(op_l + "   " + op_r)
    print("-" * (lhs_w + rhs_w + 3))


def resolver_interactivo(eq_inicial, variable):

    eq = eq_inicial

    while True:

        print("\nEcuación actual:\n")
        mostrar_vertical(eq)

        if (eq.lhs == variable and eq.rhs.is_number) or \
           (eq.rhs == variable and eq.lhs.is_number):
            print("\nLa ecuación está resuelta.")
            break

        op = input("\nIntroduce operación o pulsa r para reiniciar la ecuación: ")

        if op == "r":
            eq = eq_inicial
            print("\nEcuación reiniciada.")
            continue

        try:
            operador = op[0]
            expr = sympify(op[1:])

            if operador == "+":
                nueva = Eq(eq.lhs + expr, eq.rhs + expr)
            elif operador == "-":
                nueva = Eq(eq.lhs - expr, eq.rhs - expr)
            elif operador == "*":
                nueva = Eq(eq.lhs * expr, eq.rhs * expr)
            elif operador == "/":
                nueva = Eq(eq.lhs / expr, eq.rhs / expr)
            else:
                print("Operación no válida.")
                continue

            nueva = Eq(simplify(nueva.lhs), simplify(nueva.rhs))

            print()
            mostrar_vertical(eq, operador, expr)
            mostrar_vertical(nueva)

            eq = nueva

        except Exception:
            print("No se pudo interpretar la operación.")

#%% Main

escribir_lento("Bienvenido, agente. \n")
escribir_lento("Hemos descubierto que ya se conoce la fecha del examen del tema de ecuaciones. Sin embargo, esta información ha sido codificada.\n")
escribir_lento("Tu misión es resolver las ecuaciones. Si juntas las soluciones en orden, obtendrás la fecha.")

for ecuacion in ecuaciones:
    resolver_interactivo(ecuacion, x)
    time.sleep(1)

escribir_lento("¡Increíble! Has resuelto todas las soluciones. Deberías obtener la fecha si juntas los números.")