````markdown
# MathTutor Web App

Aplicación web educativa para practicar matemáticas de **1° a 8° básico (Chile)**.  
Permite generar **ejercicios automáticos** usando modelos de lenguaje (Groq + Gemini con fallback), verificar respuestas y obtener explicaciones paso a paso.

---

## 🚀 Características
- Desarrollada en **Python + Streamlit**.
- Generación automática de ejercicios y problemas matemáticos:
  - Problemas contextualizados (con historias).
  - Ejercicios directos (álgebra, ecuaciones, inecuaciones).
- Compatible con el currículum chileno (1° a 8° básico).
- Retroalimentación automática y explicaciones paso a paso.
- Manejo de decimales con **coma o punto**.
- Efectos visuales de **Streamlit** (`st.balloons` 🎈).
- Fallback de IA:
  - **Primero Groq** (`llama-3.1-8b-instant`).
  - Si falla, pasa a **Gemini** (`models/gemini-2.5-flash`).

---

## 📂 Estructura de carpetas

```bash
mathtutor-web/
│
├── app.py               # Aplicación principal (Streamlit)
├── llm_utils.py         # Utilidades para Groq/Gemini
├── requirements.txt     # Dependencias del proyecto
├── .env.example         # Ejemplo de configuración de API Keys
├── .gitignore           # Ignora claves, venv, caches, etc.
├── README.md            # Documentación del proyecto
└── .streamlit/          # Configs locales de Streamlit (opcional)
````

---

## ⚙️ Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/mathtutor-web.git
   cd mathtutor-web
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   # o
   source venv/bin/activate  # Linux/Mac
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

---

## 🔑 Configuración de claves

1. Copia el archivo de ejemplo:

   ```bash
   cp .env.example .env
   ```

2. Edita `.env` con tus claves de API:

```ini
# Orden de fallback: Groq → Gemini
LLM_ORDER=groq,gemini

# Groq API (https://console.groq.com/keys)
GROQ_API_KEY=tu_clave_de_groq

# Gemini API (https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=tu_clave_de_gemini

# Opcionales
# GROQ_MODEL=llama-3.1-8b-instant
# GEMINI_MODEL=models/gemini-2.5-flash
```

⚠️ **Nunca subas tu `.env` a GitHub**. Solo versiona `.env.example`.

---

## ▶️ Uso

Ejecuta la app con Streamlit:

```bash
streamlit run app.py
```

Se abrirá en tu navegador en [http://localhost:8501](http://localhost:8501).

---

## 📝 Instrucciones para estudiantes

* Escribe **solo el resultado numérico** si el problema lo pide (ej: `3`).
* Para ecuaciones, puedes responder con `x = 3` o simplemente `3`.
* Se aceptan decimales con **coma** (`3,5`) o con **punto** (`3.5`).
* Lee bien el enunciado antes de responder.

---

## 📦 Dependencias principales

* [streamlit](https://streamlit.io) → UI web.
* [python-dotenv](https://pypi.org/project/python-dotenv/) → Manejo de variables de entorno.
* [groq](https://pypi.org/project/groq/) → Cliente para la API de Groq.
* [google-generativeai](https://pypi.org/project/google-generativeai/) → Cliente para Gemini API.
* [pandas](https://pandas.pydata.org/) → (opcional, si agregas gráficos).
* [plotly](https://plotly.com/python/) → (opcional, para visualizaciones interactivas).

---

## 🌍 Despliegue

Puedes desplegar la aplicación en:

* **Streamlit Community Cloud** (gratis):

  1. Sube tu repo a GitHub.
  2. En [share.streamlit.io](https://share.streamlit.io), conecta el repo.
  3. Define variables en **Secrets**:

     ```toml
     GROQ_API_KEY="tu_clave"
     GEMINI_API_KEY="tu_clave"
     LLM_ORDER="groq,gemini"
     ```

* **Otros servicios**: Render, Railway, etc.

---

## 👨‍💻 Autor

**Luis Alberto Bustos Quezada**
Analista de Datos & BI | Estudiante Ingeniería en Data Science

📍 Punta Arenas, Chile

