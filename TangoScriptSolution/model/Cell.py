from enum import Enum
from typing import Tuple, Optional


class Condicion(Enum):
    """Enum para las condiciones de la celda"""
    IGUAL = 0
    MULTIPLICAR = 1


class DireccionCondicion(Enum):
    """Enum para la dirección de la condición"""
    ARRIBA = "arriba"
    ABAJO = "abajo"
    IZQUIERDA = "izquierda"
    DERECHA = "derecha"


class Celda:
    def __init__(self,
                 fila: int = 0,
                 columna: int = 0,
                 clicks: int = 0,
                 condicion: Condicion = None,
                 direccion_condicion: DireccionCondicion = None):
        """
        Inicializa una celda

        Args:
            fila (int): Índice de fila
            columna (int): Índice de columna
            clicks (int): Número de clicks realizados
            condicion (Condicion): Condicionante actual de la celda
            direccion_condicion (DireccionCondicion): Dirección de la condición
        """
        self.fila = fila
        self.columna = columna
        self.clicks = clicks
        self.condicion = condicion
        self.direccion_condicion = direccion_condicion

    @property
    def indices(self) -> Tuple[int, int]:
        """Retorna los índices como tupla (fila, columna)"""
        return (self.fila, self.columna)

    @property
    def indices_string(self) -> str:
        """Retorna los índices como string"""
        return f"({self.fila},{self.columna})"

    def hacer_click(self) -> None:
        """Incrementa el contador de clicks"""
        self.clicks += 1

    def establecer_condicion(self, condicion: Condicion,
                             direccion: DireccionCondicion = None) -> None:
        """
        Establece la condición y dirección de la celda

        Args:
            condicion (Condicion): Nueva condición
            direccion (DireccionCondicion): Nueva dirección
        """
        self.condicion = condicion
        self.direccion_condicion = direccion

    def es_vacia(self) -> bool:
        """Verifica si la celda está vacía"""
        return self.clicks == 0

    def es_sol(self) -> bool:
        """Verifica si la celda contiene un sol"""
        return self.clicks == 1

    def es_luna(self) -> bool:
        """Verifica si la celda contiene una luna"""
        return self.clicks == 2

    def tiene_signo(self) -> bool:
        """Verifica si la celda contiene un signo (= o X)"""
        return self.condicion in [Condicion.IGUAL, Condicion.MULTIPLICAR]

    def __str__(self) -> str:
        """Representación string de la celda"""
        simbolos = {
            Condicion.IGUAL: "=",
            Condicion.MULTIPLICAR: "✖️"
        }
        return f"Celda{self.indices_string}: {simbolos.get(self.condicion, '?')} [clicks: {self.clicks}]"


# Ejemplo de uso y testing
if __name__ == "__main__":
    # Crear celdas de ejemplo
    celda1 = Celda(0, 0)
    celda2 = Celda(1, 2, clicks=3, condicion=Condicion.IGUAL)
    celda3 = Celda(2, 1, condicion=Condicion.IGUAL, direccion_condicion=DireccionCondicion.ARRIBA)

    # Probar métodos
    print("=== EJEMPLOS DE USO ===")
    print(f"Celda 1: {celda1}")
    print(f"Celda 2: {celda2}")
    print(f"Celda 3: {celda3}")

    print(f"\nÍndices celda1: {celda1.indices}")
    print(f"Índices string celda2: {celda2.indices_string}")

    # Hacer clicks
    celda1.hacer_click()
    celda1.hacer_click()
    print(f"Celda1 después de 2 clicks: {celda1}")

    # Cambiar condición
    celda1.establecer_condicion(Condicion.MULTIPLICAR, DireccionCondicion.ABAJO)
    print(f"Celda1 con nueva condición: {celda1}")

    # Verificaciones
    print(f"\n¿Celda2 es sol? {celda2.es_sol()}")
    print(f"¿Celda3 tiene signo? {celda3.tiene_signo()}")
    print(f"¿Celda1 está vacía? {celda1.es_vacia()}")

    print(f"\n=== REPRESENTACIONES ===")
    print(f"str(celda2): {str(celda2)}")
    print(f"repr(celda2): {repr(celda2)}")