from flask import Flask, request, jsonify, session
from flask_cors import CORS

from asistente.asistente import (
    preguntar_ia,
    cargar_conversaciones,
    guardar_conversaciones
)

from asistente.memoria import (
    analizar_recuerdo,
    fusionar_memoria
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import json
import os
import uuid


app = Flask(__name__)

app.secret_key = "dashil-clave-desarrollo-2026"

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*",
            "allow_headers": [
                "Content-Type",
                "X-Usuario-Id"
            ],
            "methods": [
                "GET",
                "POST",
                "PUT",
                "DELETE",
                "OPTIONS"
            ]
        }
    }
)


# ==========================================
# ARCHIVO DE CHATS DE LA PÁGINA WEB
# ==========================================

ARCHIVO_CHATS = os.path.join(
    os.path.dirname(__file__),
    "chats.json"
)

# ==========================================
# ARCHIVO DE USUARIOS
# ==========================================

ARCHIVO_USUARIOS = os.path.join(
    os.path.dirname(__file__),
    "usuarios.json"
)


## ==========================================
# MEMORIA DE DASHIL POR USUARIO
# ==========================================

CARPETA_MEMORIA_USUARIOS = os.path.join(
    os.path.dirname(__file__),
    "memoria",
    "usuarios"
)


def obtener_archivo_memoria_usuario(usuario_id):

    carpeta_usuario = os.path.join(
        CARPETA_MEMORIA_USUARIOS,
        usuario_id
    )

    os.makedirs(
        carpeta_usuario,
        exist_ok=True
    )

    return os.path.join(
        carpeta_usuario,
        "datos_usuario.json"
    )


def cargar_memoria_usuario(usuario_id):

    archivo = obtener_archivo_memoria_usuario(
        usuario_id
    )

    if not os.path.exists(archivo):

        memoria_inicial = {
            "proyectos": {},
            "preferencias": [],
            "habilidades": [],
            "intereses": [],
            "informacion_personal": []
        }

        with open(
            archivo,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                memoria_inicial,
                f,
                ensure_ascii=False,
                indent=2
            )

        return memoria_inicial

    try:

        with open(
            archivo,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return {
            "proyectos": {},
            "preferencias": [],
            "habilidades": [],
            "intereses": [],
            "informacion_personal": []
        }


def guardar_memoria_usuario(
    usuario_id,
    datos
):

    archivo = obtener_archivo_memoria_usuario(
        usuario_id
    )

    with open(
        archivo,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            datos,
            f,
            ensure_ascii=False,
            indent=2
        )



conversaciones = cargar_conversaciones()

# ==========================================
# CARGAR USUARIOS
# ==========================================

def cargar_usuarios():

    if not os.path.exists(ARCHIVO_USUARIOS):
        return {}

    try:

        with open(
            ARCHIVO_USUARIOS,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(archivo)

    except Exception:

        return {}


# ==========================================
# GUARDAR USUARIOS
# ==========================================

def guardar_usuarios(usuarios):

    with open(
        ARCHIVO_USUARIOS,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            usuarios,
            archivo,
            ensure_ascii=False,
            indent=2
        )


# ==========================================
# CARGAR CHATS
# ==========================================

def cargar_chats():

    if not os.path.exists(ARCHIVO_CHATS):

        return {}

    try:

        with open(
            ARCHIVO_CHATS,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(archivo)

    except Exception:

        return {}


# ==========================================
# GUARDAR CHATS
# ==========================================

def guardar_chats(chats):

    with open(
        ARCHIVO_CHATS,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            chats,
            archivo,
            ensure_ascii=False,
            indent=2
        )


# ==========================================
# CARGAR CHATS AL INICIAR
# ==========================================

chats = cargar_chats()

usuarios = cargar_usuarios()

# ==========================================
# OBTENER ID DEL USUARIO
# ==========================================



def obtener_usuario_id():

    usuario_id = request.headers.get(
        "X-Usuario-Id"
    )

    print("X-Usuario-Id recibido:", usuario_id)

    if not usuario_id:
        return None

    return usuario_id


# ==========================================
# ESTADO
# ==========================================

@app.route("/api/estado", methods=["GET"])
def estado():

    return jsonify({
        "estado": "online",
        "nombre": "Dashil"
    })

# ==========================================
# REGISTRO
# ==========================================

@app.route("/api/registro", methods=["POST"])
def registrar_usuario():

    datos = request.get_json()

    if not datos:
        return jsonify({
            "error": "No se recibieron datos."
        }), 400


    nombre = datos.get(
        "nombre",
        ""
    ).strip()

    email = datos.get(
        "email",
        ""
    ).strip().lower()

    password = datos.get(
        "password",
        ""
    )


    if not nombre:
        return jsonify({
            "error": "El nombre es obligatorio."
        }), 400


    if not email:
        return jsonify({
            "error": "El correo es obligatorio."
        }), 400


    if len(password) < 6:
        return jsonify({
            "error": "La contraseña debe tener al menos 6 caracteres."
        }), 400


    # Comprobar si ya existe el correo

    for usuario in usuarios.values():

        if usuario.get("email") == email:

            return jsonify({
                "error": "Ya existe una cuenta con este correo."
            }), 409


    usuario_id = str(uuid.uuid4())


    usuarios[usuario_id] = {

        "id": usuario_id,

        "nombre": nombre,

        "email": email,

        "password_hash":
            generate_password_hash(password)

    }


    guardar_usuarios(usuarios)


    return jsonify({

        "mensaje": "Cuenta creada correctamente.",

        "usuario": {
            "id": usuario_id,
            "nombre": nombre,
            "email": email
        }

    }), 201

# ==========================================
# LOGIN
# ==========================================

@app.route("/api/login", methods=["POST"])
def iniciar_sesion():

    datos = request.get_json()

    if not datos:
        return jsonify({
            "error": "No se recibieron datos."
        }), 400


    email = datos.get(
        "email",
        ""
    ).strip().lower()

    password = datos.get(
        "password",
        ""
    )


    usuario_encontrado = None


    for usuario in usuarios.values():

        if usuario.get("email") == email:

            usuario_encontrado = usuario

            break


    if not usuario_encontrado:

        return jsonify({
            "error": "Correo o contraseña incorrectos."
        }), 401


    password_hash = usuario_encontrado.get(
        "password_hash",
        ""
    )


    if not check_password_hash(
        password_hash,
        password
    ):

        return jsonify({
            "error": "Correo o contraseña incorrectos."
        }), 401


    # Crear sesión después de validar todo
    session["usuario_id"] = usuario_encontrado["id"]


    return jsonify({

        "mensaje": "Inicio de sesión correcto.",

        "usuario": {

            "id":
                usuario_encontrado["id"],

            "nombre":
                usuario_encontrado["nombre"],

            "email":
                usuario_encontrado["email"]

        }

    })

# ==========================================
# OBTENER LISTA DE CONVERSACIONES
# ==========================================

@app.route("/api/conversaciones", methods=["GET"])
def obtener_conversaciones():

    usuario_id = obtener_usuario_id()

    if not usuario_id:

        return jsonify({
            "error": "Usuario no identificado."
        }), 401


    chats_usuario = chats.get(
        usuario_id,
        {}
    )


    resultado = []


    for chat_id, chat in chats_usuario.items():

        resultado.append({

            "id": chat_id,

            "titulo": chat.get(
                "titulo",
                "Nueva conversación"
            ),

            "fijado": chat.get(
                "fijado",
                False
            )

        })


    resultado.sort(
        key=lambda chat: not chat["fijado"]
    )


    return jsonify(resultado)


# ==========================================
# CREAR NUEVA CONVERSACIÓN
# ==========================================

@app.route("/api/conversaciones", methods=["POST"])
def crear_conversacion():

    usuario_id = obtener_usuario_id()

    if not usuario_id:

        return jsonify({
            "error": "Usuario no identificado."
        }), 401


    if usuario_id not in chats:

        chats[usuario_id] = {}


    chat_id = str(uuid.uuid4())


    chats[usuario_id][chat_id] = {

        "titulo": "Nueva conversación",

        "fijado": False,

        "mensajes": []

    }


    guardar_chats(chats)


    return jsonify({

        "id": chat_id,

        "titulo": "Nueva conversación"

    })


# ==========================================
# OBTENER UNA CONVERSACIÓN
# ==========================================

@app.route(
    "/api/conversaciones/<chat_id>",
    methods=["GET"]
)
def obtener_conversacion(chat_id):

    usuario_id = obtener_usuario_id()

    if not usuario_id:

        return jsonify({
            "error": "Usuario no identificado."
        }), 401


    chats_usuario = chats.get(
        usuario_id,
        {}
    )


    if chat_id not in chats_usuario:

        return jsonify({
            "error": "La conversación no existe."
        }), 404


    return jsonify(
        chats_usuario[chat_id]
    )


# ==========================================
# RENOMBRAR CONVERSACIÓN
# ==========================================

@app.route(
    "/api/conversaciones/<chat_id>",
    methods=["PUT"]
)
def renombrar_conversacion(chat_id):

    usuario_id = obtener_usuario_id()

    if not usuario_id:

        return jsonify({
            "error": "Usuario no identificado."
        }), 401


    chats_usuario = chats.get(
        usuario_id,
        {}
    )


    if chat_id not in chats_usuario:

        return jsonify({
            "error": "La conversación no existe."
        }), 404


    datos = request.get_json()


    if not datos or "titulo" not in datos:

        return jsonify({
            "error": "No se recibió el nuevo título."
        }), 400


    titulo = datos["titulo"].strip()


    if not titulo:

        return jsonify({
            "error": "El título no puede estar vacío."
        }), 400


    # Limitar longitud

    titulo = titulo[:60]


    chats_usuario[chat_id]["titulo"] = titulo


    guardar_chats(chats)


    return jsonify({
        "id": chat_id,
        "titulo": titulo
    })


# ==========================================
# FIJAR / DESFIJAR CONVERSACIÓN
# ==========================================

@app.route(
    "/api/conversaciones/<chat_id>/fijar",
    methods=["PUT"]
)
def fijar_conversacion(chat_id):

    usuario_id = obtener_usuario_id()

    if not usuario_id:

        return jsonify({
            "error": "Usuario no identificado."
        }), 401


    chats_usuario = chats.get(
        usuario_id,
        {}
    )


    if chat_id not in chats_usuario:

        return jsonify({
            "error": "La conversación no existe."
        }), 404


    chat = chats_usuario[chat_id]


    estado_actual = chat.get(
        "fijado",
        False
    )


    if not estado_actual:

        conversaciones_fijadas = sum(

            1

            for conversacion
            in chats_usuario.values()

            if conversacion.get(
                "fijado",
                False
            )

        )


        if conversaciones_fijadas >= 3:

            return jsonify({
                "error":
                "Solo puedes fijar hasta 3 conversaciones."
            }), 400


    chat["fijado"] = not estado_actual


    guardar_chats(chats)


    return jsonify({

        "id": chat_id,

        "fijado": chat["fijado"]

    })

# ==========================================
# ELIMINAR CONVERSACIÓN
# ==========================================

@app.route(
    "/api/conversaciones/<chat_id>",
    methods=["DELETE"]
)
def eliminar_conversacion(chat_id):

    usuario_id = obtener_usuario_id()

    if not usuario_id:

        return jsonify({
            "error": "Usuario no identificado."
        }), 401


    chats_usuario = chats.get(
        usuario_id,
        {}
    )


    if chat_id not in chats_usuario:

        return jsonify({
            "error": "La conversación no existe."
        }), 404


    del chats_usuario[chat_id]


    guardar_chats(chats)


    return jsonify({
        "mensaje":
        "Conversación eliminada correctamente."
    })

# ==========================================
# CHAT
# ==========================================

@app.route("/api/chat", methods=["POST"])
def chat():


    print(">>> ENTRÓ UNA PETICIÓN A /api/chat")
    
    usuario_id = obtener_usuario_id()

    print(">>> USUARIO RECIBIDO:", usuario_id)

    if not usuario_id:

        return jsonify({
            "error": "Usuario no identificado."
        }), 401


    datos_usuario = cargar_memoria_usuario(
        usuario_id
    )


    if usuario_id not in chats:

        chats[usuario_id] = {}


    chats_usuario = chats[usuario_id]

    try:

        

        datos = request.get_json()


        if not datos:

            return jsonify({
                "error": "No se recibieron datos."
            }), 400


        mensaje = datos.get(
            "mensaje",
            ""
        ).strip()


        chat_id = datos.get(
            "chat_id"
        )


        if not mensaje:

            return jsonify({
                "error": "El mensaje está vacío."
            }), 400


        # ==================================
        # CREAR CHAT SI NO EXISTE
        # ==================================

        if not chat_id or chat_id not in chats_usuario:

            chat_id = str(uuid.uuid4())

            chats_usuario[chat_id] = {

                "titulo": mensaje[:40],

                "fijado": False,

                "mensajes": []

            }


        chat = chats_usuario[chat_id]


        # ==================================
        # CONVERTIR MENSAJES PARA DASHIL
        # ==================================

        conversaciones_dashil = []


        mensajes = chat["mensajes"]


        for i in range(
            0,
            len(mensajes),
            2
        ):

            if i + 1 < len(mensajes):

                usuario = mensajes[i]

                respuesta = mensajes[i + 1]


                if (
                    usuario["rol"] == "usuario"
                    and respuesta["rol"] == "dashil"
                ):

                    conversaciones_dashil.append({

                        "usuario": usuario["contenido"],

                        "ia": respuesta["contenido"]

                    })


        # ==================================
        # PREGUNTAR A DASHIL
        # ==================================

        print()
        print("Usuario:", mensaje)
        print("Dashil está pensando...")


        respuesta = preguntar_ia(
        mensaje,
        conversaciones_dashil,
        datos_usuario
        )

        nuevos_recuerdos = analizar_recuerdo(
        mensaje,
        respuesta,
        datos_usuario
        )

        print(
            "Nuevos recuerdos detectados:",
            nuevos_recuerdos
        )

        

        print("Dashil:", respuesta)

        


        # ==================================
        # GUARDAR MENSAJES
        # ==================================

        chat["mensajes"].append({

            "rol": "usuario",

            "contenido": mensaje

        })


        chat["mensajes"].append({

            "rol": "dashil",

            "contenido": respuesta

        })


        # ==================================
        # TÍTULO
        # ==================================

        if chat["titulo"] == "Nueva conversación":

            chat["titulo"] = mensaje[:40]


        # ==================================
        # GUARDAR
        # ==================================

        guardar_chats(chats)


        return jsonify({

            "chat_id": chat_id,

            "respuesta": respuesta

        })


    except Exception as error:

        print("ERROR:")

        print(error)


        return jsonify({

            "error": str(error)

        }), 500


# ==========================================
# EJECUTAR SERVIDOR
# ==========================================

if __name__ == "__main__":

    print("=" * 50)

    print("              DASHIL WEB")

    print("=" * 50)

    print(
        "Servidor: "
        "http://127.0.0.1:5000"
    )

    print("Estado: ONLINE")

    print("=" * 50)


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )