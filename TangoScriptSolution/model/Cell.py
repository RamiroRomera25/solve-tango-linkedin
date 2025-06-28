from enum import Enum
from typing import Tuple, Dict, Optional, List


class Condicion(Enum):
    IGUAL = 0
    MULTIPLICAR = 1


class DireccionCondicion(Enum):
    ARRIBA = "arriba"
    ABAJO = "abajo"
    IZQUIERDA = "izquierda"
    DERECHA = "derecha"


class Celda:
    def __init__(self,
                 fila: int = 0,
                 columna: int = 0,
                 clicks: int = 0,
                 condiciones: Optional[Dict[DireccionCondicion, Condicion]] = None):
        self.fila = fila
        self.columna = columna
        self.clicks = clicks
        self.condiciones: Dict[DireccionCondicion, Condicion] = condiciones or {}

    @property
    def indices(self) -> Tuple[int, int]:
        return (self.fila, self.columna)

    @property
    def indices_string(self) -> str:
        return f"({self.fila},{self.columna})"

    def hacer_click(self) -> None:
        self.clicks += 1

    def establecer_condicion(self, condicion: Condicion,
                             direccion: DireccionCondicion) -> None:
        """Agrega o actualiza una condición para una dirección dada"""
        self.condiciones[direccion] = condicion

    def eliminar_condicion(self, direccion: DireccionCondicion) -> None:
        """Elimina condición para una dirección dada, si existe"""
        if direccion in self.condiciones:
            del self.condiciones[direccion]

    def obtener_condicion(self, direccion: DireccionCondicion) -> Optional[Condicion]:
        """Devuelve la condición para una dirección o None si no existe"""
        return self.condiciones.get(direccion)

    def es_vacia(self) -> bool:
        return self.clicks == 0

    def es_sol(self) -> bool:
        return self.clicks == 1

    def es_luna(self) -> bool:
        return self.clicks == 2

    def tiene_signo(self) -> bool:
        return any(cond in [Condicion.IGUAL, Condicion.MULTIPLICAR] for cond in self.condiciones.values())

    def obtener_condiciones(self) -> List[Tuple[DireccionCondicion, Condicion, bool]]:
        """
        Retorna una lista con las condiciones actuales, cada item es una tupla:
        (direccion, condicion, cumplida)
        Por ahora cumplida siempre False, porque no se guarda ese estado.
        """
        condiciones = []
        for direccion, condicion in self.condiciones.items():
            cumplida = False
            condiciones.append((direccion, condicion, cumplida))
        return condiciones

    def __str__(self) -> str:
        simbolos = {
            Condicion.IGUAL: "=",
            Condicion.MULTIPLICAR: "✖️"
        }
        conds_str = ", ".join(
            f"{simbolos.get(cond, '?')}({dir.value})"
            for dir, cond in self.condiciones.items()
        ) if self.condiciones else "No condiciones"
        return f"Celda{self.indices_string}: {conds_str} [clicks: {self.clicks}]"


# Ejemplo rápido
if __name__ == "__main__":
    celda = Celda(1, 1, clicks=1)
    celda.establecer_condicion(Condicion.IGUAL, DireccionCondicion.DERECHA)
    celda.establecer_condicion(Condicion.MULTIPLICAR, DireccionCondicion.ABAJO)
    # celda.eliminar_condicion(DireccionCondicion.ABAJO)
    print(celda)
