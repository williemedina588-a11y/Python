from asistente.chat import DashilChat


def main():

    print("=" * 60)
    print("                 DASHIL")
    print("=" * 60)
    print("Asistente personal con IA")
    print("Escribe 'salir' para cerrar.")
    print("Escribe 'borrar memoria' para eliminar la memoria.")
    print()

    dashil = DashilChat()

    while True:

        mensaje = input("Tú: ").strip()

        if mensaje.lower() == "salir":
            print("Dashil: Hasta luego.")
            break

        if mensaje.lower() == "borrar memoria":
            dashil.borrar_memoria()
            print("Dashil: Memoria borrada.")
            print()
            continue

        if not mensaje:
            continue

        print("\nDashil está pensando...\n")

        try:

            respuesta = dashil.responder(mensaje)

            print("Dashil:", respuesta)
            print()

        except Exception as error:

            print("Dashil: Ocurrió un error.")
            print(error)
            print()


if __name__ == "__main__":
    main()