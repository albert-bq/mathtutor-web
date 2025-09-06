# Math Game Web App - Groq + Gemini Fallback
# Autor: Luis Alberto Bustos Quezada

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()  # ⬅️ primero carga .env

from llm_utils import generar_problema, verificar_respuesta, ayuda_paso_a_paso  # ⬅️ luego importa


# ============================
# CONFIGURACION DE LA PAGINA
# ============================
st.set_page_config(
    page_title="Juego Matemático - LLM",
    page_icon="🧠",
    layout="centered"
)

# ============================
# CURRÍCULUM CHILENO - MATEMÁTICAS
# ============================
temas_por_grado = {
    "1° Básico": [
        "Conteo hasta 100",
        "Sumas y restas simples",
        "Figuras geométricas básicas",
        "Patrones",
        "Medidas no estandarizadas"
    ],
    "2° Básico": [
        "Números hasta 1.000",
        "Sumas y restas con llevadas",
        "Multiplicación como suma reiterada",
        "Mitades y cuartos",
        "Reloj y monedas"
    ],
    "3° Básico": [
        "Multiplicación y división (tablas)",
        "Fracciones unitarias",
        "Perímetro de figuras simples",
        "Medición estandarizada"
    ],
    "4° Básico": [
        "Números hasta 1.000.000",
        "Multiplicación y división (mayores)",
        "Fracciones equivalentes",
        "Decimales (introducción)",
        "Área de cuadrados y rectángulos"
    ],
    "5° Básico": [
        "Operaciones con fracciones",
        "Operaciones con decimales",
        "Porcentajes (básico)",
        "Triángulos y cuadriláteros",
        "Coordenadas en el plano",
        "Área de figuras planas"
    ],
    "6° Básico": [
        "Fracciones, decimales y porcentajes (equivalencia)",
        "Proporcionalidad y razones",
        "Perímetro y área (polígonos)",
        "Volumen de prismas",
        "Gráficos y tablas simples"
    ],
    "7° Básico": [
        "Números enteros",
        "Potencias y raíces simples",
        "Razones y proporciones",
        "Ecuaciones de primer grado (simples)",
        "Área y volumen (cuerpos)",
        "Estadística: media, mediana y moda"
    ],
    "8° Básico": [
        "Álgebra (expresiones)",
        "Ecuaciones lineales",
        "Inecuaciones",
        "Funciones lineales (introducción)",
        "Volumen (cilindros, conos, esferas)",
        "Probabilidades",
        "Porcentajes avanzados"
    ]
}

# ============================
# INTERFAZ STREAMLIT
# ============================
st.title("🧠 Juego Matemático con LLM")
st.markdown("Resuelve ejercicios de matemáticas alineados al currículum chileno. Selecciona tu grado, tema y tipo de ejercicio.")

st.markdown("""
### ℹ️ Instrucciones de uso
- Escribe **solo el resultado numérico** si el problema lo pide (ej: `3`).
- Si es una ecuación, debes responder con la variable que se está pidiendo, por ejemplo `x = 3`.  
- Para respuestas decimales puedes usar **coma** (3,5) o **punto** (3.5).
- Lee bien el enunciado y usa el formato más sencillo posible.
""")


col1, col2, col3 = st.columns(3)
with col1:
    grado = st.selectbox("📘 Grado:", list(temas_por_grado.keys()))
with col2:
    tema = st.selectbox("📚 Tema:", temas_por_grado[grado] if grado else [])
with col3:
    tipo = st.selectbox("✏️ Tipo de ejercicio:", ["Automático", "Problema contextualizado", "Ejercicio directo"])

error_debug = st.empty()

# ============================
# BOTON GENERAR EJERCICIO
# ============================
if grado and tema:
    if st.button("🎯 Generar ejercicio"):
        try:
            with st.spinner("Generando ejercicio..."):
                st.session_state.problema = generar_problema(grado, tema, tipo)
                st.session_state.respuesta_usuario = ""
                if not st.session_state.problema:
                    st.warning("No se recibió contenido. Intenta de nuevo o cambia de modelo/tema.")
        except Exception as e:
            error_debug.error(f"❌ Error al generar: {e}")

# ============================
# MOSTRAR PROBLEMA
# ============================
if "problema" in st.session_state and st.session_state.problema:
    st.markdown("### 🔹 Problema generado:")
    problema_md = st.session_state.problema.get("problema", "").replace("\\n", "\n").replace("  ", " ")

    st.markdown(
        f"""
<div style='background-color:#0e1117;padding:1rem;border-radius:0.5rem;border-left:5px solid #2f81f7'>
<p style='color:#ffffff'>{problema_md}</p>
</div>
""",
        unsafe_allow_html=True
    )

    # Entrada de respuesta
    st.session_state.respuesta_usuario = st.text_input("✏️ Tu respuesta:", value=st.session_state.get("respuesta_usuario", ""))

    # Botón verificar
    if st.button("✅ Verificar respuesta"):
        feedback = verificar_respuesta(
            st.session_state.problema.get("problema", ""),
            st.session_state.problema.get("respuesta_correcta", ""),
            st.session_state.respuesta_usuario,
            grado
        )

        if feedback:
            if feedback.get("es_correcta", False):
                mensaje_correcto = (feedback.get("mensaje", "")).replace("\\n", "\n").replace("```", "")
                st.markdown(
                    f"""
<div style='background-color:#1e4023;padding:1rem;border-radius:0.5rem;border-left:5px solid #27ae60'>
<p style='color:#d4f4dd;font-size:1.1rem'>
🎉 <strong>¡Correcto!</strong><br>{mensaje_correcto}
</p>
</div>
""",
                    unsafe_allow_html=True
                )
                st.balloons()
            else:
                feedback_md = (feedback.get("mensaje", "")).replace("\\n", "\n").replace("```", "")
                st.markdown(
                    f"""
<div style='background-color:#2f1f1f;padding:1rem;border-radius:0.5rem;border-left:5px solid #d35f5f'>
<p style='color:#ffffff'>🤔 {feedback_md}</p>
</div>
""",
                    unsafe_allow_html=True
                )

# ============================
# FOOTER
# ============================
st.markdown("---")
st.caption("Desarrollado por Luis A. Bustos Quezada | Fallback Groq+Gemini | Framework: Streamlit")
