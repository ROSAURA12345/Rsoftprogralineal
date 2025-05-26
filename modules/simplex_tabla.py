import numpy as np
import pandas as pd

def parse_input(objetivo):
    c = []
    objetivo = objetivo.replace('-', '+-')
    for term in objetivo.split('+'):
        term = term.strip()
        if 'x' in term:
            val = term.split('x')[0]
            val = val if val not in ['', '+', '-'] else val + '1'
            c.append(float(val))
    return np.array(c)

def parse_restricciones(restricciones):
    A, b, signos = [], [], []
    for restr in restricciones.strip().splitlines():
        restr = restr.strip()
        if "<=" in restr:
            lhs, rhs = restr.split("<=")
            signo = "<="
        elif ">=" in restr:
            lhs, rhs = restr.split(">=")
            signo = ">="
        elif "=" in restr:
            lhs, rhs = restr.split("=")
            signo = "="
        else:
            continue

        lhs = lhs.replace('-', '+-')
        coefs = []
        for term in lhs.split('+'):
            term = term.strip()
            if 'x' in term:
                val = term.split('x')[0]
                val = val if val not in ['', '+', '-'] else val + '1'
                coefs.append(float(val))
        A.append(coefs)
        b.append(float(rhs.strip()))
        signos.append(signo)
    return np.array(A), np.array(b), signos

def construir_tabla(A, b, c, signos):
    m, n = A.shape
    num_slack = signos.count('<=')
    num_artificial = signos.count('>=') + signos.count('=')

    total_vars = n + num_slack + num_artificial
    tabla = np.zeros((m, total_vars + 1))

    slack_index = n
    artificial_index = n + num_slack
    base = []

    for i in range(m):
        tabla[i, :n] = A[i]
        if signos[i] == '<=':
            tabla[i, slack_index] = 1
            base.append(slack_index)
            slack_index += 1
        elif signos[i] == '>=':
            tabla[i, slack_index] = -1
            tabla[i, artificial_index] = 1
            base.append(artificial_index)
            slack_index += 1
            artificial_index += 1
        elif signos[i] == '=':
            tabla[i, artificial_index] = 1
            base.append(artificial_index)
            artificial_index += 1
        tabla[i, -1] = b[i]

    cj = np.zeros(total_vars + 1)
    cj[:len(c)] = c

    return tabla, cj, base

def calcular_z(tabla, cj, base_idx):
    base_matrix = tabla[:, base_idx]
    z = base_matrix @ cj[base_idx]
    zj = np.dot(z, tabla[:, :-1])
    zcj = cj[:-1] - zj
    return np.append(zcj, 0)

def iteracion_simplex(tabla, cj, base_idx):
    zcj = calcular_z(tabla, cj, base_idx)
    explicacion = ""

    if np.all(zcj[:-1] <= 1e-8):
        explicacion = "Todos los valores de Cj - Zj son <= 0. Se alcanzó la solución óptima."
        return tabla, base_idx, zcj, True, None, None, explicacion

    col_piv = np.argmax(zcj[:-1])
    explicacion += f"Se elige la columna pivote x{col_piv + 1} con Cj - Zj: {zcj[col_piv]:.2f}.\n"

    ratios = []
    for i in range(len(tabla)):
        if tabla[i, col_piv] > 1e-8:
            ratio = tabla[i, -1] / tabla[i, col_piv]
            ratios.append(ratio)
        else:
            ratios.append(np.inf)

    fila_piv = np.argmin(ratios)
    explicacion += f"Fila pivote: {fila_piv + 1} con razón mínima {ratios[fila_piv]:.2f}\n"

    pivote = tabla[fila_piv, col_piv]
    tabla[fila_piv, :] /= pivote
    for i in range(len(tabla)):
        if i != fila_piv:
            tabla[i, :] -= tabla[i, col_piv] * tabla[fila_piv, :]

    base_idx[fila_piv] = col_piv
    terminado = np.all(calcular_z(tabla, cj, base_idx)[:-1] <= 1e-8)

    return tabla, base_idx, calcular_z(tabla, cj, base_idx), terminado, col_piv, fila_piv, explicacion

def resolver_simplex_tabla(objetivo, restricciones, tipo="max"):
    c = parse_input(objetivo)
    A, b, signos = parse_restricciones(restricciones)

    if tipo == 'min':
        c = -c

    tabla, cj, base_idx = construir_tabla(A, b, c, signos)
    pasos = []
    terminado = False
    iteracion = 0

    while not terminado:
        iteracion += 1
        tabla, base_idx, zcj, terminado, col_piv, fila_piv, explicacion = iteracion_simplex(tabla, cj, base_idx)

        columnas = [f"x{i+1}" for i in range(tabla.shape[1] - 1)] + ["RHS"]
        base_vars = [f"x{i+1}" for i in base_idx]
        df = pd.DataFrame(tabla, columns=columnas, index=base_vars)
        df.loc['Cj-Zj'] = zcj

        pasos.append((iteracion, df.copy(), col_piv, fila_piv, explicacion))

    valor_optimo = tabla[:, -1].dot(cj[base_idx])
    if tipo == 'min':
        valor_optimo = -valor_optimo

    return pasos, valor_optimo
