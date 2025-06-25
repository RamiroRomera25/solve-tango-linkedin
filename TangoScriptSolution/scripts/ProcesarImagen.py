import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder = "white"
TEMPLATE_PATH = os.path.join(BASE_DIR, "images", folder)
ENTRADA_PATH = os.path.join(BASE_DIR, "images", "entrada.PNG")

# Cargar templates
templates = {
    0: cv2.imread(os.path.join(TEMPLATE_PATH, "empty.PNG"), 0),
    1: cv2.imread(os.path.join(TEMPLATE_PATH, "sol.PNG"), 0),
    2: cv2.imread(os.path.join(TEMPLATE_PATH, "luna.PNG"), 0),
    # 3: cv2.imread(os.path.join(TEMPLATE_PATH, "multiply.PNG"), 0),
    # 4: cv2.imread(os.path.join(TEMPLATE_PATH, "equal.PNG"), 0),
}

# Verificar templates cargados
for key, tpl in templates.items():
    if tpl is None:
        print(f"Template {key} no se pudo cargar")
        exit(1)

image = cv2.imread(ENTRADA_PATH, 0)
if image is None:
    print("❌ Imagen principal no se pudo cargar")
    exit(1)

rows, cols = 6, 6
cell_h = image.shape[0] // rows
cell_w = image.shape[1] // cols

matriz_resultado = []

def main():
    for i in range(rows):
        fila = []
        for j in range(cols):
            celda = image[i * cell_h:(i + 1) * cell_h, j * cell_w:(j + 1) * cell_w]

            mejor_key = None
            mejor_valor = -1

            for key, tpl in templates.items():
                res = cv2.matchTemplate(celda, tpl, cv2.TM_CCOEFF_NORMED)
                val = np.max(res)
                if val > mejor_valor:
                    mejor_valor = val
                    mejor_key = key

            fila.append(mejor_key)
        matriz_resultado.append(fila)

    for fila in matriz_resultado:
        print(fila)

if __name__ == '__main__':
    main()