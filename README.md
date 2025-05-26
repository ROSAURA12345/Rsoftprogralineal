✅ Entregable para tu tarea:
📁 1. Archivo de despliegue con su respectivo manual
✅ Carpeta comprimida (.zip) con toda la estructura del proyecto

✅ Archivo README.md que actúa como manual de uso (lo genero abajo)

✅ Código fuente completo

✅ Listo para ejecutar localmente

📝 README.md (Manual + Descripción del proyecto)
markdown
Copiar
Editar
# 🧮 Programación Lineal - Método Gráfico y Simplex

Este proyecto web permite resolver problemas de programación lineal utilizando tres enfoques:
- ✅ Método Gráfico (visual e interactivo)
- ✅ Método Simplex Directo (rápido y automático)
- ✅ Método Simplex con Tabla (educativo y paso a paso)

---

## 📌 Desarrollado por:
**Rosaura Yana Pari**

## 📅 Actividad:
**Programación Lineal – Método Gráfico**  
**Profesor:** Milton Edward Humpiri Flores  
**Fecha de entrega:** Domingo 25 de mayo – 11:59 PM

---

## 🚀 Cómo ejecutar la aplicación

### 1. Clona o descomprime el proyecto
Asegúrate de tener Python instalado.

### 2. Crea un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
3. Instala las dependencias
bash
Copiar
Editar
pip install -r requirements.txt
4. Ejecuta la aplicación
bash
Copiar
Editar
python app.py
5. Abre en el navegador:
arduino
Copiar
Editar
http://localhost:5000
📁 Estructura del Proyecto
pgsql
Copiar
Editar
RSOFTPROGRALINEAL/
├── app.py
├── requirements.txt
├── modules/
│   ├── grafico.py
│   ├── simplex.py
│   ├── simplex_tabla.py
├── utils/
│   └── parser.py
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── metodo_grafico.html
│   ├── metodo_simplex.html
│   └── metodo_simplex_tabla.html
└── static/
    └── style.css (incrustado)
💡 Funcionalidades
🔷 Método gráfico con graficación interactiva usando Plotly.

🔶 Simplex directo con Scipy.

🔸 Simplex con tabla paso a paso usando Pandas.

🖥️ Interfaz clara, educativa e intuitiva.

📱 Totalmente responsive (adaptado a móviles).

🧠 Tecnologías Utilizadas
Flask

NumPy, SciPy

Matplotlib, Plotly

Pandas

HTML5, CSS3, Bootstrap 5