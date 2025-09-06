
MathTutor Web App

Aplicación web educativa para practicar matemáticas de 1° a 8° básico (Chile).
Permite generar ejercicios automáticos usando modelos de lenguaje (Groq + Gemini con fallback), verificar respuestas y obtener explicaciones paso a paso.

🚀 Características

Desarrollada en Python + Streamlit.
Generación automática de ejercicios y problemas matemáticos:
Problemas contextualizados (con historias).
Ejercicios directos (álgebra, ecuaciones, inecuaciones).
Compatible con el currículum chileno (1° a 8° básico).
Retroalimentación automática y explicaciones paso a paso.
Manejo de decimales con coma o punto.
Efectos visuales de Streamlit (st.balloons 🎈).
Fallback de IA:
Primero Groq (llama-3.1-8b-instant).
Si falla, pasa a Gemini (models/gemini-2.5-flash).

📂 Estructura de carpetas


Bash


mathtutor-web/
│
├── app.py               # Aplicación principal (Streamlit)
├── llm_utils.py         # Utilidades para Groq/Gemini
├── requirements.txt     # Dependencias del proyecto
├──.env.example         # Ejemplo de configuración de API Keys
├──.gitignore           # Ignora claves, venv, caches, etc.
├── README.md            # Documentación del proyecto
└──.streamlit/          # Configs locales de Streamlit (opcional)



⚙️ Instalación

Clona el repositorio:

Bash


git clone https://github.com/tu-usuario/mathtutor-web.git
cd mathtutor-web


Crea y activa un entorno virtual:

Bash


python -m venv venv
venv\Scripts\activate   # Windows
# o
source venv/bin/activate  # Linux/Mac


Instala las dependencias:

Bash


pip install -r requirements.txt



🔑 Configuración de claves

Copia el archivo de ejemplo:

Bash


cp.env.example.env


Edita .env con tus claves de API:

Ini, TOML


# Orden de fallback: Groq → Gemini
LLM_ORDER=groq,gemini

# Groq API (https://console.groq.com/keys)
GROQ_API_KEY=tu_clave_de_groq

# Gemini API (https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=tu_clave_de_gemini

# Opcionales
# GROQ_MODEL=llama-3.1-8b-instant
# GEMINI_MODEL=models/gemini-2.5-flash


⚠️ Nunca subas tu .env a GitHub. Solo versiona .env.example.

▶️ Uso

Ejecuta la app con Streamlit:

Bash


streamlit run app.py


Se abrirá en tu navegador en http://localhost:8501.

📝 Instrucciones para estudiantes

Escribe solo el resultado numérico si el problema lo pide (ej: 3).
Para ecuaciones, puedes responder con x = 3 o simplemente 3.
Se aceptan decimales con coma (3,5) o con punto (3.5).
Lee bien el enunciado antes de responder.

📦 Dependencias principales

streamlit → UI web.
python-dotenv → Manejo de variables de entorno.
groq → Cliente para la API de Groq.
google-generativeai → Cliente para Gemini API.
pandas → (opcional, si agregas gráficos).
plotly → (opcional, para visualizaciones interactivas).

🌍 Despliegue

Puedes desplegar la aplicación en:
Streamlit Community Cloud (gratis):
Sube tu repo a GitHub.
En share.streamlit.io, conecta el repo.
Define variables en Secrets:
Ini, TOML
GROQ_API_KEY="tu_clave"
GEMINI_API_KEY="tu_clave"
LLM_ORDER="groq,gemini"


Otros servicios: Render, Railway, etc.

👨‍💻 Autor

Luis Alberto Bustos Quezada
Analista de Datos & BI | Estudiante Ingeniería en Data Science
📍 Punta Arenas, Chile
