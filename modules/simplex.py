from scipy.optimize import linprog
import numpy as np

def parse_funcion_objetivo(obj):
    """
    Parsea una función objetivo tipo "6x1+12x2+8x3" y devuelve [6, 12, 8]
    """
    obj = obj.replace('-', '+-')
    coef = []
    for term in obj.split('+'):
        term = term.strip()
        if 'x' in term:
            val = term.split('x')[0]
            if val in ['', '+']:
                val = '1'
            elif val == '-':
                val = '-1'
            try:
                coef.append(float(val))
            except ValueError:
                coef.append(0.0)
    return coef

def parse_restricciones(restrs):
    """
    Parsea restricciones tipo "2x1+3x2+4x3<=120"
    Devuelve:
    - A (matriz de coeficientes)
    - b (lado derecho)
    - signos (relaciones)
    """
    A, b, signos = [], [], []
    for restr in restrs.strip().splitlines():
        restr = restr.strip()
        if not restr:
            continue

        if '<=' in restr:
            lhs, rhs = restr.split('<=')
            signo = '<='
        elif '>=' in restr:
            lhs, rhs = restr.split('>=')
            signo = '>='
        elif '=' in restr:
            lhs, rhs = restr.split('=')
            signo = '='
        else:
            continue

        lhs = lhs.replace('-', '+-')
        coefs = []
        for term in lhs.split('+'):
            term = term.strip()
            if 'x' in term:
                val = term.split('x')[0]
                if val in ['', '+']:
                    val = '1'
                elif val == '-':
                    val = '-1'
                try:
                    coefs.append(float(val))
                except ValueError:
                    coefs.append(0.0)
        A.append(coefs)
        b.append(float(rhs.strip()))
        signos.append(signo)

    return A, b, signos

def resolver_simplex(objetivo, restricciones, tipo='max'):
    """
    Resuelve el problema de programación lineal por el método simplex usando scipy.optimize.linprog.
    Admite restricciones tipo <=, >= y =.
    """

    c = parse_funcion_objetivo(objetivo)
    A, b, signos = parse_restricciones(restricciones)

    # Determinar máximo número de variables
    max_vars = max(len(row) for row in A + [c])
    c += [0.0] * (max_vars - len(c))
    A = [row + [0.0] * (max_vars - len(row)) for row in A]

    A_ub, b_ub, A_eq, b_eq = [], [], [], []

    for i, signo in enumerate(signos):
        if signo == '<=':
            A_ub.append(A[i])
            b_ub.append(b[i])
        elif signo == '>=':
            A_ub.append([-a for a in A[i]])
            b_ub.append(-b[i])
        elif signo == '=':
            A_eq.append(A[i])
            b_eq.append(b[i])

    # Preparar vector de costos
    c_vector = -np.array(c) if tipo == 'max' else np.array(c)

    res = linprog(
        c=c_vector,
        A_ub=A_ub if A_ub else None,
        b_ub=b_ub if b_ub else None,
        A_eq=A_eq if A_eq else None,
        b_eq=b_eq if b_eq else None,
        method='highs'
    )

    if res.success:
        solucion = [f"x{i+1} = {v:.2f}" for i, v in enumerate(res.x)]
        valor_optimo = res.fun if tipo == 'min' else -res.fun
        return (
            "✅ <strong>Solución encontrada:</strong><br>" +
            "<br>".join(solucion) +
            f"<br><br>🔹 <strong>Valor óptimo:</strong> {valor_optimo:.2f}"
        )
    else:
        return "❌ <strong>No se encontró una solución óptima.</strong>"
