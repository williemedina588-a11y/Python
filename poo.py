# Ejemplo corto de POO: clase padre y dos hijas
# Define una clase padre Animal, y dos clases hijas Perro y Gato.
# Se muestran atributos y métodos heredados y propios.

class Animal:
    """Clase padre con atributos y métodos comunes."""
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def describir(self):
        return f"{self.nombre}, {self.edad} años"

    def hablar(self):
        return "Sonido genérico"

class Perro(Animal):
    """Clase hija: Perro añade un método propio."""
    def hablar(self):
        return "Guau"

    def mover_colita(self):
        return f"{self.nombre} mueve la cola"

class Gato(Animal):
    """Clase hija: Gato añade un método propio."""
    def hablar(self):
        return "Miau"

    def ronronear(self):
        return f"{self.nombre} está ronroneando"

# Flujo: crear instancias y mostrar uso de métodos heredados y propios
if __name__ == "__main__":
    perro = Perro("Rex", 5)
    gato = Gato("Luna", 3)

    print(perro.describir())      # método heredado
    print(perro.hablar())         # método sobreescrito
    print(perro.mover_colita())   # método propio

    print(gato.describir())       # heredado
    print(gato.hablar())          # sobreescrito
    print(gato.ronronear())       # propio
