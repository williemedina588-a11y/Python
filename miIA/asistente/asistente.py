import json
import os
import requests


MODELO = "llama3.2"

CARPETA_MEMORIA = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "memoria"
)

ARCHIVO_CONVERSACIONES = os.path.join(
    CARPETA_MEMORIA,
    "conversaciones.json"
)

ARCHIVO_DATOS_USUARIO = os.path.join(
    CARPETA_MEMORIA,
    "datos_usuario.json"
)


PERSONALIDAD = """
Tu nombre es Dashil.

Eres el asistente personal del usuario.

Tu objetivo es ayudarlo de manera práctica, clara, inteligente y honesta.

Puedes ayudar con:
- estudios
- programación
- matemáticas
- documentos
- investigación
- ideas de negocios
- organización
- aprendizaje
- análisis de información
- finanzas de manera educativa
- desarrollo personal
- tecnología
- resolución de problemas

Responde siempre en español, salvo que el usuario solicite otro idioma.

No inventes información.
Si no sabes algo, dilo claramente.

No prometas ganancias económicas.
No realices acciones importantes sin autorización del usuario.

Explica las cosas de forma sencilla cuando el usuario no tenga experiencia.

Cuando la pregunta sea sencilla, responde de forma sencilla.
No hagas respuestas excesivamente largas cuando no sean necesarias.
"""


def cargar_conversaciones():

    if not os.path.exists(ARCHIVO_CONVERSACIONES):
        return []

    try:
        with open(
            ARCHIVO_CONVERSACIONES,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(archivo)

    except Exception:
        return []


def guardar_conversaciones(conversaciones):

    limite_palabras = 440_000

    conversaciones_filtradas = []

    total_palabras = 0

    for conversacion in reversed(conversaciones):

        texto = (
            conversacion.get("usuario", "")
            + " "
            + conversacion.get("ia", "")
        )

        palabras = texto.split()

        cantidad = len(palabras)

        if total_palabras + cantidad > limite_palabras:

            palabras_disponibles = (
                limite_palabras - total_palabras
            )

            if palabras_disponibles <= 0:
                break

            texto_recortado = " ".join(
                palabras[:palabras_disponibles]
            )

            conversaciones_filtradas.append({
                "usuario": texto_recortado,
                "ia": ""
            })

            break

        conversaciones_filtradas.append(
            conversacion
        )

        total_palabras += cantidad

    conversaciones_filtradas.reverse()

    os.makedirs(
        CARPETA_MEMORIA,
        exist_ok=True
    )

    with open(
        ARCHIVO_CONVERSACIONES,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            conversaciones_filtradas,
            archivo,
            ensure_ascii=False,
            indent=2
        )


def cargar_datos_usuario():

    if not os.path.exists(ARCHIVO_DATOS_USUARIO):
        return {}

    try:
        with open(
            ARCHIVO_DATOS_USUARIO,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(archivo)

    except Exception:
        return {}


def guardar_datos_usuario(datos):

    os.makedirs(
        CARPETA_MEMORIA,
        exist_ok=True
    )

    with open(
        ARCHIVO_DATOS_USUARIO,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=2
        )


def preguntar_ia(
    mensaje,
    conversaciones,
    datos_usuario
):

    contexto = ""

    for conversacion in conversaciones[-10:]:

        contexto += f"""
Usuario: {conversacion["usuario"]}
Dashil: {conversacion["ia"]}
"""


    recuerdos = json.dumps(
        datos_usuario,
        ensure_ascii=False,
        indent=2
    )


    instrucciones_memoria = f"""
MEMORIA PERMANENTE DEL USUARIO:

{recuerdos}

REGLAS PARA UTILIZAR LA MEMORIA:

1. Utiliza la memoria cuando sea relevante para responder.

2. Si el usuario pregunta qué sabes, qué recuerdas o pregunta
por alguno de sus proyectos, revisa primero esta memoria.

3. No digas que no tienes información si existe información
relevante en la memoria.

4. No inventes información que no esté en la memoria.

5. Puedes relacionar información de diferentes recuerdos cuando
claramente pertenecen al mismo proyecto.

6. Si una información de la memoria no tiene relación con la
pregunta actual, ignórala.
"""


    prompt = f"""
{PERSONALIDAD}

{instrucciones_memoria}

CONVERSACIONES RECIENTES:

{contexto}

MENSAJE ACTUAL DEL USUARIO:

{mensaje}

Antes de responder, analiza silenciosamente la memoria y las
conversaciones recientes.

Si el usuario pregunta sobre un proyecto, utiliza los datos
relacionados con ese proyecto.

Si el usuario pregunta qué recuerdas sobre él o sobre alguno
de sus proyectos, menciona la información que realmente esté
guardada.

Responde directamente al usuario.

Si la pregunta es sencilla, responde de forma sencilla.

No inventes información ni recuerdos.
"""


    respuesta = requests.post(
        "http://localhost:11434/api/generate",

        json={
            "model": MODELO,
            "prompt": prompt,
            "stream": False
        },

        timeout=300
    )


    respuesta.raise_for_status()

    datos = respuesta.json()

    return datos["response"]


def main():

    print("=" * 60)
    print("                 DASHIL")
    print("=" * 60)

    print("Asistente personal con IA")
    print("Escribe 'salir' para cerrar.")
    print("Escribe 'borrar memoria' para eliminar conversaciones.")
    print()

    conversaciones = cargar_conversaciones()
    datos_usuario = cargar_datos_usuario()


    while True:

        mensaje = input("Tú: ").strip()


        if mensaje.lower() == "salir":

            print("Hasta luego.")
            break


        if mensaje.lower() == "borrar memoria":

            conversaciones = []

            guardar_conversaciones(
                conversaciones
            )

            print("Memoria de conversaciones borrada.")
            print()

            continue


        if not mensaje:
            continue


        print("\nDashil está pensando...\n")


        try:

            respuesta = preguntar_ia(
                mensaje,
                conversaciones,
                datos_usuario
            )


            print("Dashil:", respuesta)
            print()


            conversaciones.append({
                "usuario": mensaje,
                "ia": respuesta
            })


            guardar_conversaciones(
                conversaciones
            )


        except requests.exceptions.ConnectionError:

            print(
                "Dashil no pudo conectarse con Ollama."
            )

            print(
                "Comprueba que Ollama esté instalado "
                "y funcionando."
            )


        except Exception as error:

            print("Ocurrió un error:")
            print(error)


if __name__ == "__main__":
    main()