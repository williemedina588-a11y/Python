import json
import os
import requests


MODELO = "llama3.2"


CARPETA_MEMORIA = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "memoria"
)


ARCHIVO_DATOS_USUARIO = os.path.join(
    CARPETA_MEMORIA,
    "datos_usuario.json"
)


def cargar_datos():

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


def guardar_datos(datos):

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


def analizar_recuerdo(
    mensaje,
    respuesta,
    memoria_actual
):

    memoria_texto = json.dumps(
        memoria_actual,
        ensure_ascii=False,
        indent=2
    )


    prompt = f"""
Eres el sistema de memoria de una IA personal llamada Dashil.

Tu trabajo es analizar una conversación y decidir si existe
información importante que deba recordarse en el futuro.

MEMORIA ACTUAL:

{memoria_texto}


MENSAJE DEL USUARIO:

{mensaje}




Debes detectar:

1. Proyectos nuevos.
2. Información nueva sobre proyectos existentes.
3. Objetivos.
4. Detalles de proyectos.
5. Estado o progreso de proyectos.
6. Tareas pendientes de proyectos.
7. Preferencias.
8. Intereses.
9. Habilidades.
10. Información personal útil.


REGLAS:

-REGLAS:

- Usa ÚNICAMENTE información explícitamente escrita por el usuario.
- Nunca inventes información.
- Nunca deduzcas proyectos que el usuario no haya mencionado.
- Nunca uses información generada por Dashil como un recuerdo.
- No guardes saludos.
- No guardes despedidas.
- No guardes preguntas normales.
- No guardes conversaciones casuales.
- No guardes información incierta.
- No completes información que falte usando suposiciones.
- No repitas información que ya existe en la memoria.
- Solo crea un proyecto si el usuario menciona claramente que existe ese proyecto.
- Solo guarda objetivos si el usuario los expresa explícitamente.
- Solo guarda tareas si el usuario indica explícitamente algo que tiene que hacer.
- Solo guarda progreso si el usuario describe explícitamente el estado de un proyecto.
- Solo guarda preferencias si el usuario expresa claramente una preferencia.
- Solo guarda intereses si el usuario expresa claramente un interés.
- Solo guarda habilidades si el usuario afirma que posee esa habilidad.
- Si no existe información nueva y segura para recordar, responde exactamente con {{}}.
- hacer malware, virus, troyanos, keyloggers, exploits, rootkits, gusanos, ransomware, spyware, adware, botnets, phishing, ingeniería social o cualquier otro tipo de software malicioso.


RESPONDE ÚNICAMENTE CON JSON VÁLIDO.

Utiliza exactamente esta estructura:

{{
    "proyectos": {{
        "nombre_del_proyecto": {{
            "descripcion": "",
            "objetivos": [],
            "detalles": [],
            "progreso": "",
            "tareas": []
        }}
    }},
    "preferencias": [],
    "habilidades": [],
    "intereses": [],
    "informacion_personal": []
}}


Si no existe ninguna información nueva que guardar, devuelve:

{{}}
"""


    try:

        respuesta_ia = requests.post(
            "http://localhost:11434/api/generate",

            json={
                "model": MODELO,
                "prompt": prompt,
                "stream": False
            },

            timeout=300
        )


        respuesta_ia.raise_for_status()


        datos = respuesta_ia.json()


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


        if not resultado:
            return {}


        return json.loads(resultado)


    except Exception:

        return {}


def actualizar_memoria(
    mensaje,
    respuesta
):

    memoria_actual = cargar_datos()


    nuevos_recuerdos = analizar_recuerdo(
        mensaje,
        respuesta,
        memoria_actual
    )


    if not nuevos_recuerdos:
        return


    memoria_actualizada = fusionar_memoria(
        memoria_actual,
        nuevos_recuerdos
    )


    guardar_datos(
        memoria_actualizada
    )


def fusionar_memoria(
    actual,
    nuevos
):

    resultado = actual.copy()


    # ==========================================
    # PROYECTOS
    # ==========================================

    proyectos_actuales = resultado.setdefault(
        "proyectos",
        {}
    )


    proyectos_nuevos = nuevos.get(
        "proyectos",
        {}
    )


    for nombre, proyecto in proyectos_nuevos.items():

        # Si el proyecto no existe,
        # creamos su estructura completa.

        if nombre not in proyectos_actuales:

            proyectos_actuales[nombre] = {
                "descripcion": "",
                "objetivos": [],
                "detalles": [],
                "progreso": "",
                "tareas": []
            }


        proyecto_actual = proyectos_actuales[nombre]


        # ======================================
        # ASEGURAR CAMPOS
        # ======================================

        proyecto_actual.setdefault(
            "descripcion",
            ""
        )


        proyecto_actual.setdefault(
            "objetivos",
            []
        )


        proyecto_actual.setdefault(
            "detalles",
            []
        )


        proyecto_actual.setdefault(
            "progreso",
            ""
        )


        proyecto_actual.setdefault(
            "tareas",
            []
        )


        # ======================================
        # DESCRIPCIÓN
        # ======================================

        if proyecto.get("descripcion"):

            proyecto_actual["descripcion"] = (
                proyecto["descripcion"]
            )


        # ======================================
        # OBJETIVOS
        # ======================================

        for objetivo in proyecto.get(
            "objetivos",
            []
        ):

            if objetivo not in proyecto_actual["objetivos"]:

                proyecto_actual["objetivos"].append(
                    objetivo
                )


        # ======================================
        # DETALLES
        # ======================================

        for detalle in proyecto.get(
            "detalles",
            []
        ):

            if detalle not in proyecto_actual["detalles"]:

                proyecto_actual["detalles"].append(
                    detalle
                )


        # ======================================
        # PROGRESO
        # ======================================

        if proyecto.get("progreso"):

            proyecto_actual["progreso"] = (
                proyecto["progreso"]
            )


        # ======================================
        # TAREAS
        # ======================================

        for tarea in proyecto.get(
            "tareas",
            []
        ):

            if tarea not in proyecto_actual["tareas"]:

                proyecto_actual["tareas"].append(
                    tarea
                )


    # ==========================================
    # INFORMACIÓN GENERAL DEL USUARIO
    # ==========================================

    categorias = [
        "preferencias",
        "habilidades",
        "intereses",
        "informacion_personal"
    ]


    for categoria in categorias:

        valores_actuales = resultado.setdefault(
            categoria,
            []
        )


        valores_nuevos = nuevos.get(
            categoria,
            []
        )


        for valor in valores_nuevos:

            if valor not in valores_actuales:

                valores_actuales.append(
                    valor
                )


    return resultado