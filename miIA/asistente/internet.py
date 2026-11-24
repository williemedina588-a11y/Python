import requests


# Instancia pública de SearXNG
SEARXNG_URL = "https://search.bus-hit.me/search"


def buscar_en_internet(consulta, cantidad=5):

    parametros = {
        "q": consulta,
        "format": "json",
        "language": "es",
        "safesearch": 1
    }

    try:

        respuesta = requests.get(
            SEARXNG_URL,
            params=parametros,
            timeout=20
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

        resultados = []

        for resultado in datos.get("results", [])[:cantidad]:

            resultados.append({
                "titulo": resultado.get(
                    "title",
                    ""
                ),

                "url": resultado.get(
                    "url",
                    ""
                ),

                "descripcion": resultado.get(
                    "content",
                    ""
                )
            })

        return resultados

    except requests.exceptions.Timeout:

        print("La búsqueda tardó demasiado.")

        return []

    except requests.exceptions.RequestException as error:

        print("Error al conectarse con Internet:")
        print(error)

        return []

    except ValueError:

        print(
            "La respuesta de Internet no tenía "
            "un formato válido."
        )

        return []