from typing import Iterator, List, Optional

from Cell import Celda, DireccionCondicion, Condicion


class MatrizCeldas:
    def __init__(self, iconos: List[List[int]], signosH: List[List[Optional[str]]], signosV: List[List[Optional[str]]]):
        self.filas = len(iconos)
        self.columnas = len(iconos[0])
        self.matriz: List[List[Celda]] = [
            [Celda(fila, columna, clicks=iconos[fila][columna]) for columna in range(self.columnas)]
            for fila in range(self.filas)
        ]

        # Aplicar condiciones horizontales
        for fila in range(len(signosH)):
            for columna in range(len(signosH[0])):
                signo = signosH[fila][columna]
                if signo:
                    celda = self.matriz[fila][columna]
                    celda_siguiente_h = self.matriz[fila][columna + 1]

                    condicion = self._parsear_signo(signo)
                    celda.establecer_condicion(condicion, DireccionCondicion.DERECHA)
                    celda_siguiente_h.establecer_condicion(condicion, DireccionCondicion.IZQUIERDA)

        # Aplicar condiciones verticales
        for fila in range(len(signosV)):
            for columna in range(len(signosV[0])):
                signo = signosV[fila][columna]
                if signo:
                    celda = self.matriz[fila][columna]
                    celda_siguiente_v = self.matriz[fila + 1][columna]

                    condicion = self._parsear_signo(signo)
                    celda.establecer_condicion(condicion, DireccionCondicion.ABAJO)
                    celda_siguiente_v.establecer_condicion(condicion, DireccionCondicion.ARRIBA)

    def _parsear_signo(self, signo: str) -> Condicion:
        if signo == '=':
            return Condicion.IGUAL
        elif signo.lower() == 'x':
            return Condicion.MULTIPLICAR
        else:
            raise ValueError(f"Signo desconocido: {signo}")

    def get_celda(self, fila: int, columna: int) -> Celda:
        return self.matriz[fila][columna]

    def get_fila(self, fila: int) -> List[Celda]:
        return self.matriz[fila]

    def get_columna(self, columna: int) -> List[Celda]:
        return [self.matriz[f][columna] for f in range(self.filas)]

    def get_sub_fila(self, fila: int, desde: int, hasta: int) -> List[Celda]:
        return self.matriz[fila][desde:hasta]

    def get_sub_columna(self, columna: int, desde: int, hasta: int) -> List[Celda]:
        return [self.matriz[f][columna] for f in range(desde, hasta)]

    def __iter__(self) -> Iterator[Celda]:
        return MatrizCeldasIterator(self)

    def to_string(self) -> str:
        filas_texto = []
        ancho_celda = 5

        def formatear_clicks(celda: Celda) -> str:
            return str(celda.clicks).center(ancho_celda)

        def formatear_condicion(condicion: Optional[Condicion], direccion: Optional[DireccionCondicion]) -> str:
            if condicion is None:
                return " ".center(ancho_celda)
            simbolo = {
                Condicion.IGUAL: "=",
                Condicion.MULTIPLICAR: "✖️"
            }.get(condicion, "?")
            direccion_simbolo = {
                DireccionCondicion.ARRIBA: "↑",
                DireccionCondicion.ABAJO: "↓",
                DireccionCondicion.DERECHA: "→",
                DireccionCondicion.IZQUIERDA: "←"
            }.get(direccion, " ")
            return (simbolo + direccion_simbolo).center(ancho_celda)

        separador_horizontal = "+" + ("-" * ancho_celda + "+") * self.columnas

        for fila in range(self.filas):
            filas_texto.append(separador_horizontal)

            # Línea de clicks
            fila_clicks = "|"
            for col in range(self.columnas):
                fila_clicks += formatear_clicks(self.matriz[fila][col]) + "|"
            filas_texto.append(fila_clicks)

            # Línea de condiciones horizontales
            fila_cond_h = "|"
            for col in range(self.columnas):
                condicion_h = None
                direccion_h = None

                celda = self.matriz[fila][col]

                # Verificamos si la condición horizontal está en esta celda con dirección DERECHA
                if celda.obtener_condicion(DireccionCondicion.DERECHA) is not None:
                    condicion_h = celda.obtener_condicion(DireccionCondicion.DERECHA)
                    direccion_h = DireccionCondicion.DERECHA

                # Si no, chequeamos si la condición horizontal está en la celda a la izquierda con dirección DERECHA
                elif col > 0:
                    celda_izq = self.matriz[fila][col - 1]
                    if celda_izq.obtener_condicion(DireccionCondicion.DERECHA) is not None:
                        condicion_h = celda_izq.obtener_condicion(DireccionCondicion.DERECHA)
                        direccion_h = DireccionCondicion.IZQUIERDA

                fila_cond_h += formatear_condicion(condicion_h, direccion_h) + "|"
            filas_texto.append(fila_cond_h)

            # Línea de condiciones verticales
            fila_cond_v = "|"
            for col in range(self.columnas):
                condicion_v = None
                direccion_v = None

                celda = self.matriz[fila][col]

                # Verificamos si la condición vertical está en esta celda con dirección ABAJO
                if celda.obtener_condicion(DireccionCondicion.ABAJO) is not None:
                    condicion_v = celda.obtener_condicion(DireccionCondicion.ABAJO)
                    direccion_v = DireccionCondicion.ABAJO

                # Si no, chequeamos si la condición vertical está en la celda arriba con dirección ABAJO
                elif fila > 0:
                    celda_arriba = self.matriz[fila - 1][col]
                    if celda_arriba.obtener_condicion(DireccionCondicion.ABAJO) is not None:
                        condicion_v = celda_arriba.obtener_condicion(DireccionCondicion.ABAJO)
                        direccion_v = DireccionCondicion.ARRIBA

                fila_cond_v += formatear_condicion(condicion_v, direccion_v) + "|"
            filas_texto.append(fila_cond_v)

        filas_texto.append(separador_horizontal)
        return "\n".join(filas_texto)


class MatrizCeldasIterator:
    def __init__(self, matriz: MatrizCeldas):
        self.matriz = matriz
        self.filas = matriz.filas
        self.columnas = matriz.columnas

        # Contadores separados para cada fase
        self._index_filas = 0
        self._index_columnas = 0

        # Estado: 'filas' o 'columnas'
        self._fase = 'filas'

        # Para evitar devolver celdas repetidas
        self._visitadas = set()

    def __iter__(self):
        return self

    def __next__(self) -> Celda:
        if self._fase == 'filas':
            if self._index_filas >= self.filas * self.columnas:
                # Cambiamos a la fase columnas
                self._fase = 'columnas'
                self._index_columnas = 0
            else:
                fila = self._index_filas // self.columnas
                col = self._index_filas % self.columnas
                self._index_filas += 1
                return self.matriz.matriz[fila][col]

        if self._fase == 'columnas':
            if self._index_columnas >= self.filas * self.columnas:
                raise StopIteration
            col = self._index_columnas // self.filas
            fila = self._index_columnas % self.filas
            self._index_columnas += 1
            return self.matriz.matriz[fila][col]


if __name__ == "__main__":
    iconos = [
        [0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 2, 0],
        [0, 0, 0, 2, 0, 0],
    ]

    # signosH = [
    #     [None, None, None, None, None],
    #     [None, None, None, None, None],
    #     [None, None, None, None, '='],
    #     ['x', None, None, None, None],
    #     [None, None, None, None, None],
    #     [None, None, None, None, None],
    # ]
    #
    # signosV = [
    #     [None, None, None, None, None, None],
    #     [None, None, None, None, None, '='],
    #     [None, 'x', None, None, '=', None],
    #     ['x', None, None, None, None, None],
    #     [None, None, None, None, None, None],
    # ]

    signosH = [
        ["x"]
    ]

    signosV = [
        [None, None, None, None, None, "="]
    ]

    matriz = MatrizCeldas(iconos, signosH, signosV)

    print("=== Recorriendo primero por filas, luego por columnas ===")
    for celda in matriz:
        if (len(celda.condiciones) > 0):
            print(celda)

    print(matriz.to_string())
