from asistente.internet_decision import necesita_internet


preguntas = [
    "¿Cuál es el precio actual de Bitcoin?",
    "¿Cuánto es 25 por 8?",
    "¿Qué noticias importantes hay hoy?",
    "Explícame qué es una variable en Python."
]


for pregunta in preguntas:

    resultado = necesita_internet(pregunta)

    print()
    print("Pregunta:", pregunta)
    print("¿Necesita Internet?:", resultado)