from asistente.internet import buscar_en_internet


consulta = input(
    "¿Qué quieres buscar en Internet?: "
)


print("\nBuscando...\n")


resultados = buscar_en_internet(
    consulta
)


if not resultados:

    print("No se encontraron resultados.")

else:

    for numero, resultado in enumerate(
        resultados,
        start=1
    ):

        print("=" * 60)

        print(
            f"Resultado {numero}"
        )

        print(
            "Título:",
            resultado["titulo"]
        )

        print(
            "URL:",
            resultado["url"]
        )

        print(
            "Descripción:",
            resultado["descripcion"]
        )

    print("=" * 60)