import matplotlib
matplotlib.use('Agg')
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
import itertools
import io
import base64
from matplotlib.patches import Polygon

def parse_funcion_objetivo(obj):
    obj = obj.replace('-', '+-')
    coef = [0, 0]
    for term in obj.split('+'):
        term = term.strip()
        if 'x1' in term:
            val = term.replace('x1', '')
            coef[0] = float(val) if val not in ['', '+', '-'] else float(val + '1')
        elif 'x2' in term:
            val = term.replace('x2', '')
            coef[1] = float(val) if val not in ['', '+', '-'] else float(val + '1')
    return coef

def parse_restricciones(restrs):
    restricciones = []
    for restr in restrs.strip().splitlines():
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
        a, b = 0, 0
        for term in lhs.split('+'):
            if 'x1' in term:
                a = float(term.replace('x1', ''))
            elif 'x2' in term:
                b = float(term.replace('x2', ''))
        restricciones.append((a, b, signo, float(rhs)))
    return restricciones

def punto_interseccion(r1, r2):
    a1, b1, _, c1 = r1
    a2, b2, _, c2 = r2
    A = np.array([[a1, b1], [a2, b2]])
    B = np.array([c1, c2])
    try:
        x = np.linalg.solve(A, B)
        return x if np.all(x >= 0) else None
    except np.linalg.LinAlgError:
        return None

def cumple_todas(punto, restricciones):
    x, y = punto
    for a, b, signo, c in restricciones:
        val = a*x + b*y
        if signo == '<=' and val > c + 1e-6:
            return False
        elif signo == '>=' and val < c - 1e-6:
            return False
        elif signo == '=' and abs(val - c) > 1e-6:
            return False
    return True

def ordenar_puntos(puntos):
    centro = np.mean(puntos, axis=0)
    return sorted(puntos, key=lambda p: np.arctan2(p[1] - centro[1], p[0] - centro[0]))

def resolver_metodo_grafico(objetivo, restricciones, tipo):
    c = parse_funcion_objetivo(objetivo)
    restr = parse_restricciones(restricciones)

    puntos_candidatos = []

    # Intersección entre pares de restricciones
    for r1, r2 in itertools.combinations(restr, 2):
        p = punto_interseccion(r1, r2)
        if p is not None:
            puntos_candidatos.append(tuple(p))

    # Intersecciones con ejes
    for a, b, signo, rhs in restr:
        if a != 0:
            x0 = rhs / a
            if x0 >= 0:
                puntos_candidatos.append((x0, 0))
        if b != 0:
            y0 = rhs / b
            if y0 >= 0:
                puntos_candidatos.append((0, y0))

    # Filtrar puntos factibles únicos
    puntos_factibles = []
    vistos = set()
    for p in puntos_candidatos:
        key = (round(p[0], 6), round(p[1], 6))
        if key not in vistos and cumple_todas(p, restr):
            puntos_factibles.append(key)
            vistos.add(key)

    info = "<ul>"
    optimo = None
    valor_optimo = None

    if len(puntos_factibles) >= 1:
        puntos_array = np.array(puntos_factibles)
        z_vals = [c[0]*x + c[1]*y for x, y in puntos_array]
        for i, (xv, yv) in enumerate(puntos_array):
            info += f"<li>Vértice {i+1}: ({xv:.2f}, {yv:.2f}) → Z = {z_vals[i]:.2f}</li>"

        idx = np.argmin(z_vals) if tipo == 'min' else np.argmax(z_vals)
        optimo = puntos_array[idx]
        valor_optimo = z_vals[idx]
        info += "</ul>"

        traces = []
        xs, ys = zip(*puntos_factibles)
        x_range = np.linspace(0, max(xs) + 10, 500)

        for a, b, signo, rhs in restr:
            if b != 0:
                y_vals = (rhs - a * x_range) / b
                traces.append(go.Scatter(x=x_range, y=y_vals,
                                         mode='lines',
                                         name=f"{a}x1 + {b}x2 {signo} {rhs}"))
            else:
                x_val = rhs / a
                traces.append(go.Scatter(x=[x_val, x_val], y=[0, max(ys) + 10],
                                         mode='lines',
                                         name=f"{a}x1 + {b}x2 {signo} {rhs}"))

        if len(puntos_factibles) >= 3:
            ordenados = ordenar_puntos(puntos_factibles)
            x_poly = [p[0] for p in ordenados] + [ordenados[0][0]]
            y_poly = [p[1] for p in ordenados] + [ordenados[0][1]]
            traces.append(go.Scatter(x=x_poly, y=y_poly,
                                     fill='toself',
                                     fillcolor='rgba(200,200,200,0.4)',
                                     line=dict(color='gray'),
                                     name='Región Factible'))

        traces.append(go.Scatter(x=puntos_array[:, 0],
                                 y=puntos_array[:, 1],
                                 mode='markers+text',
                                 text=[f"Z={z:.2f}" for z in z_vals],
                                 name='Vértices',
                                 marker=dict(size=8)))

        traces.append(go.Scatter(x=[optimo[0]], y=[optimo[1]],
                                 mode='markers+text',
                                 name='Óptimo',
                                 marker=dict(size=12, color='red'),
                                 text=[f"Óptimo: Z={valor_optimo:.2f}"]))

        layout = go.Layout(title="Método Gráfico Interactivo",
                           xaxis=dict(title='x1'),
                           yaxis=dict(title='x2'),
                           legend=dict(x=0, y=1),
                           hovermode='closest')

        fig = go.Figure(data=traces, layout=layout)
        html_result = fig.to_html(full_html=False)
        html_result += f"<p><strong>Óptimo en:</strong> ({optimo[0]:.2f}, {optimo[1]:.2f})</p>"
        html_result += f"<p><strong>Valor óptimo:</strong> {valor_optimo:.2f}</p>"
        html_result += info
        return html_result
    else:
        return "<p style='color:red;'><strong>No hay solución factible.</strong></p>"
