# llm_utils.py — Fallback automático Groq <-> Gemini
# Usa el primero disponible/funcional según LLM_ORDER (por defecto: groq,gemini)

import os, json

from dotenv import load_dotenv
load_dotenv()

# ---------------------------
# Secrets seguros (no exige secrets.toml)
# ---------------------------
def _secret(name: str):
    try:
        import streamlit as st  # import tardío para no romper tests
        return st.secrets.get(name, None)
    except Exception:
        return None

GROQ_API_KEY   = os.getenv("GROQ_API_KEY")   or _secret("GROQ_API_KEY")   or ""
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or _secret("GEMINI_API_KEY") or ""

# Orden de preferencia (editable vía .env / secrets)
LLM_ORDER = (os.getenv("LLM_ORDER") or _secret("LLM_ORDER") or "groq,gemini").lower()
ORDER = [p.strip() for p in LLM_ORDER.split(",") if p.strip() in {"groq", "gemini"}]
if not ORDER:
    ORDER = ["groq", "gemini"]

# Modelos por proveedor (puedes cambiarlos por .env si quieres)
GROQ_MODEL   = os.getenv("GROQ_MODEL")   or _secret("GROQ_MODEL")   or "llama-3.1-8b-instant"
GEMINI_MODEL = os.getenv("GEMINI_MODEL") or _secret("GEMINI_MODEL") or "models/gemini-2.5-flash"

# ---------------------------
# Utilidades JSON / números
# ---------------------------
def _clean_json_text(text: str) -> str:
    if not text:
        return ""
    return (text.replace("```json","")
                .replace("```","")
                .replace("\\n"," ")
                .replace("\n"," ")
                .replace("”","\"").replace("“","\"").replace("’","'")
                .strip())

def normalizar_numero(valor: str) -> str:
    return (valor or "").strip().replace(",", ".")

def es_numero(valor: str) -> bool:
    try:
        float(normalizar_numero(valor))
        return True
    except Exception:
        return False

# ---------------------------
# Proveedor: Groq
# ---------------------------
def _try_groq(prompt: str) -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY no configurada")
    try:
        from groq import Groq
    except Exception as e:
        raise RuntimeError(f"Librería groq no instalada: {e}")
    client = Groq(api_key=GROQ_API_KEY)
    r = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return r.choices[0].message.content

# ---------------------------
# Proveedor: Gemini
# ---------------------------
def _try_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY no configurada")
    try:
        import google.generativeai as genai
    except Exception as e:
        raise RuntimeError(f"Librería google-generativeai no instalada: {e}")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    r = model.generate_content(prompt)
    return r.text or ""

# ---------------------------
# Router con fallback
# ---------------------------
_PROVIDERS = {
    "groq": _try_groq,
    "gemini": _try_gemini,
}

def _generate(prompt: str) -> str:
    last_err = None
    for prov in ORDER:
        try:
            return _PROVIDERS[prov](prompt)
        except Exception as e:
            last_err = e  # guarda y prueba el siguiente
    raise RuntimeError(f"No se pudo generar respuesta. Último error: {last_err}")

# ---------------------------
# Prompts
# ---------------------------
def _prompt_generar(grado: str, tema: str, tipo: str):
    if tipo == "Problema contextualizado":
        preferencia = "Genera un problema contextualizado con una historia breve y realista del día a día."
    elif tipo == "Ejercicio directo":
        preferencia = "Genera un ejercicio directo y simbólico, por ejemplo: Resuelve: 2x + 2 = 5."
    else:
        preferencia = ("Para Fracciones/Porcentajes/Proporciones/Volumen prefiere problema contextualizado; "
                       "para Álgebra/Ecuaciones/Inecuaciones prefiere ejercicio directo y simbólico.")

    return f"""
Eres un profesor de matemáticas para estudiantes de {grado}.
Crea UN ejercicio del tema: "{tema}".

El ejercicio puede ser:
- Un problema contextualizado (historia breve y clara), o
- Un ejercicio directo (p. ej., Resuelve: 2x + 2 = 5)

{preferencia}

Requisitos:
- Enunciado corto y preciso (1–3 líneas).
- Una única respuesta correcta (numérica o expresión corta).
- Nivel adecuado a {grado}.
- Español de Chile. Sin adornos.

Devuelve SOLO un JSON válido (sin texto extra, sin comentarios, sin ```):
{{
  "problema": "Texto del problema o ejercicio.",
  "respuesta_correcta": "Respuesta correcta."
}}
"""

def _prompt_verificar(problema: str, rc: str, ru: str, grado: str):
    return f"""
Evalúa la respuesta de un estudiante chileno de {grado}.

Problema: {problema}
Respuesta correcta: {rc}
Respuesta del estudiante: {ru}

Indica si es correcta. Si es incorrecta, explica brevemente por qué y cómo resolverlo correctamente, en un tono amable y claro.

Devuelve SOLO JSON (sin texto extra):
{{
  "es_correcta": true/false,
  "mensaje": "Texto explicativo breve para el estudiante."
}}
"""

def _prompt_pasos(problema: str, grado: str):
    return f"""
Explica paso a paso cómo resolver este problema matemático para un estudiante de {grado}.
Problema: {problema}

Usa pasos numerados, lenguaje amigable y claro (Chile). Devuelve solo el texto de la explicación.
"""

# ---------------------------
# API pública para app.py
# ---------------------------
def generar_problema(grado: str, tema: str, tipo: str = "Automático") -> dict:
    txt = _generate(_prompt_generar(grado, tema, tipo))
    clean = _clean_json_text(txt)
    data = json.loads(clean)
    # Por si algún modelo devuelve "respuesta"
    if "respuesta" in data and "respuesta_correcta" not in data:
        data["respuesta_correcta"] = data.pop("respuesta")
    return data

def verificar_respuesta(problema: str, respuesta_correcta: str, respuesta_usuario: str, grado: str) -> dict:
    # Comparación local numérica (acepta coma/punto)
    if es_numero(respuesta_correcta) and es_numero(respuesta_usuario):
        if float(normalizar_numero(respuesta_correcta)) == float(normalizar_numero(respuesta_usuario)):
            return {"es_correcta": True, "mensaje": "Excelente, tu resultado coincide con la respuesta correcta. ¡Sigue así! 💪"}

    txt = _generate(_prompt_verificar(problema, respuesta_correcta, respuesta_usuario, grado))
    clean = _clean_json_text(txt)
    return json.loads(clean)

def ayuda_paso_a_paso(problema: str, grado: str) -> str:
    return (_generate(_prompt_pasos(problema, grado)) or "").strip()
