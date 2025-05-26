def parse_funcion_objetivo(obj):
    """
    Convierte una función objetivo como "6x1+12x2+8x3" en [6, 12, 8]
    """
    obj = obj.replace('-', '+-')
    coef = []
    for term in obj.split('+'):
        term = term.strip()
        if 'x' in term:
            coef_val = term.split('x')[0]
            if coef_val == '':
                coef_val = '1'
            elif coef_val == '-':
                coef_val = '-1'
            coef.append(float(coef_val))
    return coef

def parse_restricciones(restrs):
    """
    Convierte restricciones como:
    "2x1+2x2+4x3<=12000"
    en ([2,2,4], '<=', 12000)
    
    Devuelve:
    - lista de listas de coeficientes (A),
    - lista de signos,
    - lista de valores del lado derecho (b)
    """
    A = []
    b = []
    signos = []
    for restr in restrs.strip().splitlines():
        restr = restr.replace(' ', '')
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
            continue  # Ignora líneas inválidas

        lhs = lhs.replace('-', '+-')
        coefs = []
        for term in lhs.split('+'):
            term = term.strip()
            if 'x' in term:
                coef_val = term.split('x')[0]
                if coef_val == '':
                    coef_val = '1'
                elif coef_val == '-':
                    coef_val = '-1'
                coefs.append(float(coef_val))
        A.append(coefs)
        b.append(float(rhs.strip()))
        signos.append(signo)

    return A, b, signos
