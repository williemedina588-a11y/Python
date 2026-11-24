from .asistente import (
    preguntar_ia,
    cargar_conversaciones,
    guardar_conversaciones,
    cargar_datos_usuario
)

from .memoria import actualizar_memoria


class DashilChat:

    def __init__(self):

        self.conversaciones = cargar_conversaciones()

        self.datos_usuario = cargar_datos_usuario()


    def responder(self, mensaje):

        respuesta = preguntar_ia(
            mensaje,
            self.conversaciones,
            self.datos_usuario
        )

        self.conversaciones.append({
            "usuario": mensaje,
            "ia": respuesta
        })

        guardar_conversaciones(
            self.conversaciones
        )

        actualizar_memoria(
            mensaje,
            respuesta
        )

        self.datos_usuario = cargar_datos_usuario()

        return respuesta


    def borrar_memoria(self):

        self.conversaciones = []

        guardar_conversaciones(
            self.conversaciones
        )