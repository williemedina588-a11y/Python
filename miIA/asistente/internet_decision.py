import requests
import json


MODELO = "llama3.2"


def necesita_internet(mensaje):

    prompt = f"""
Eres el sistema que decide si una IA personal llamada Dashil
necesita consultar Internet antes de responder.

Analiza el mensaje del usuario.

MENSAJE:

{mensaje}

Devuelve ÚNICAMENTE un JSON válido con esta estructura:

{{
    "buscar": true,
    "motivo": "explicación breve"
}}

o:

{{
    "buscar": false,
    "motivo": "explicación breve"
}}

Debes responder "buscar": true cuando la pregunta necesite
información actual, reciente, cambiante o que deba comprobarse
en Internet.

Ejemplos que normalmente requieren Internet:

- Noticias actuales.
- Clima actual o pronóstico.
- Precios actuales.
- Precio de Bitcoin u otras criptomonedas.
- Resultados deportivos recientes.
- Horarios actuales.
- Información publicada recientemente.
- Información sobre productos actuales.
- Preguntas que contengan "hoy", "ahora", "actualmente",
  "último", "última", "reciente" o expresiones similares.
- Cuando el usuario pida explícitamente buscar en Internet.

Ejemplos que normalmente NO requieren Internet:

- Operaciones matemáticas sencillas y avanzadas.
- Explicaciones de programación.
- Conversaciones normales.
- Preguntas sobre información que ya está en la memoria.
- Escritura o corrección de textos.
- Ideas y lluvia de ideas.
- Explicaciones generales que no dependan de información actual.

No inventes información.

Devuelve solamente JSON válido.
"""

    try:

        respuesta = requests.post(
            "http://localhost:11434/api/generate",

            json={
                "model": MODELO,
                "prompt": prompt,
                "stream": False
            },

            timeout=120
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

        resultado = datos["response"].strip()

        resultado = resultado.replace(
            "```json",
            ""
        )

        resultado = resultado.replace(
            "```",
            ""
        )

        resultado = resultado.strip()

        decision = json.loads(resultado)

        return decision.get(
            "buscar",
            False
        )

    except Exception:

        return False