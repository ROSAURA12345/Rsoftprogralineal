# 🧮 RSoftPrograLineal

**Sistema Web Interactivo para resolver problemas de Programación Lineal**  
🌐 Desarrollado por: **Rosaura Yana Pari**  
📘 Proyecto académico | **Docente:** Milton Edward Humpiri Flores

---

## 📌 Descripción

**RSoftPrograLineal** es una aplicación web educativa que permite resolver problemas de optimización mediante programación lineal utilizando tres enfoques:

- 📊 **Método Gráfico** (2 variables, solución visual)
- ⚙️ **Simplex Directo** (cálculo instantáneo con `scipy.optimize`)
- 📋 **Simplex con Tabla** (paso a paso educativo como en clases)

Diseñado para estudiantes y docentes de matemáticas, ingeniería, economía y afines.

---

## 🚀 Demo Local

### 1. Clona el repositorio


git clone https://github.com/ROSAURA12345/Rsoftprogralineal.git
cd Rsoftprogralineal
2. Crea entorno virtual (opcional)
bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
3. Instala las dependencias
bash
Copiar
Editar
pip install -r requirements.txt
4. Ejecuta el servidor Flask
bash
Copiar
Editar
python app.py
Abre tu navegador en: http://localhost:5000

🛠 Tecnologías Usadas
Herramienta	Uso
Python 3	Lógica de backend
Flask	Framework web ligero
NumPy / SciPy	Cálculo y optimización
Plotly / Matplotlib	Gráficos interactivos
Pandas	Tablas simplex
Bootstrap 5	Interfaz adaptable
HTML5 + CSS3	Diseño responsivo

📁 Estructura del Proyecto
pgsql
Copiar
Editar
Rsoftprogralineal/
├── app.py
├── requirements.txt
├── modules/
│   ├── grafico.py
│   ├── simplex.py
│   └── simplex_tabla.py
├── utils/
│   └── parser.py
├── templates/
│   ├── index.html
│   ├── layout.html
│   ├── metodo_grafico.html
│   ├── metodo_simplex.html
│   └── metodo_simplex_tabla.html
✨ Características
🖥️ Interfaz intuitiva y profesional

📈 Gráficos de regiones factibles con Plotly

📚 Simplex educativo paso a paso

💡 Compatible con móviles y navegadores modernos

🎓 Actividad Académica
Tarea: Programación Lineal (Método Gráfico)
Curso: Análisis Multivariado
Docente: Milton Edward Humpiri Flores
Estudiante: Rosaura Yana Pari
Fecha de entrega: 25 de mayo – 11:59 p.m.

📄 Licencia
Proyecto académico sin fines comerciales.
Puedes usar este software con fines educativos o de aprendizaje.

📬 Contacto
¿Tienes sugerencias o preguntas?

📧 [rosaura.dev@example.com] (reemplázalo si tienes uno real)
💻 GitHub: @ROSAURA12345
```bash
