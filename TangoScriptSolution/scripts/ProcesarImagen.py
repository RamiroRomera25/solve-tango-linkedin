import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder = "dark"
folderSigns = "signs"
TEMPLATE_PATH = os.path.join(BASE_DIR, "images", folder)
SIGN_PATH = os.path.join(BASE_DIR, "images", folderSigns)

ENTRADA_PATH = os.path.join(BASE_DIR, "images", "template_dark_1.PNG")

# Cargar templates
templates = {
    0: cv2.imread(os.path.join(TEMPLATE_PATH, "empty.PNG"), cv2.IMREAD_COLOR), #uso el IMREAD_COLOR para que no se convierta a escala de grises
    1: cv2.imread(os.path.join(TEMPLATE_PATH, "sol.PNG"), cv2.IMREAD_COLOR),
    2: cv2.imread(os.path.join(TEMPLATE_PATH, "luna.PNG"), cv2.IMREAD_COLOR),
    3: cv2.imread(os.path.join(SIGN_PATH, "multiply.PNG"), cv2.IMREAD_COLOR),
    4: cv2.imread(os.path.join(SIGN_PATH, "equal.PNG"), cv2.IMREAD_COLOR),
}

# Verificar templates cargados
for key, tpl in templates.items():
    if tpl is None:
        print(f"Template {key} no se pudo cargar")
        exit(1)

image = cv2.imread(ENTRADA_PATH,  cv2.IMREAD_COLOR)
if image is None:
    print("❌ Imagen principal no se pudo cargar")
    exit(1)

rows, cols = 6, 6
cell_h = image.shape[0] // rows
cell_w = image.shape[1] // cols


def es_celda_vacia(celda, umbral=0.8):
    template = templates[0]
    template_resized = cv2.resize(template, (celda.shape[1], celda.shape[0]))
    # Convertir ambos a escala de grises
    celda_gray = cv2.cvtColor(celda, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_resized, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(celda_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, score, _, _ = cv2.minMaxLoc(res)
    return score >= umbral
def detectar_signo(franja, template, umbral=0.2):
    template_resized = cv2.resize(template, (franja.shape[1], franja.shape[0]))
    franja_gray = cv2.cvtColor(franja, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_resized, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(franja_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    print(f"Score de coincidencia para signo: {np.max(res):.2f}")
    _, score, _, _ = cv2.minMaxLoc(res)
    print(f"Score de coincidencia para signo: {score >= umbral}")
    return score >= umbral

def detectar_icono(celda, umbral=0.6):
    h, w = celda.shape[:2]
    offset = int(min(h, w) * 0.1)
    celda_recortada = celda[offset:h - offset, offset:w - offset]

    max_score = -1
    mejor_id = None

    for tipo_id, template in templates.items():
        # Evita errores si el template es muy pequeño
        if template is None or template.shape[0] <= 2*offset or template.shape[1] <= 2*offset:
            continue
        tpl = template[offset:template.shape[0]-offset, offset:template.shape[1]-offset]
        # Verifica que tpl y celda_recortada tengan tamaño válido
        if tpl.size == 0 or celda_recortada.size == 0:
            continue
        tpl_resized = cv2.resize(tpl, (celda_recortada.shape[1], celda_recortada.shape[0]))

        res = cv2.matchTemplate(celda_recortada, tpl_resized, cv2.TM_CCOEFF_NORMED)
        _, score, _, _ = cv2.minMaxLoc(res)

        if score > max_score:
            max_score = score
            mejor_id = tipo_id

    return mejor_id if max_score >= umbral else None
matriz_resultado = []

def main():
    for i in range(rows):
        fila = []
        for j in range(cols):
            y1, y2 = i * cell_h, (i + 1) * cell_h
            x1, x2 = j * cell_w, (j + 1) * cell_w
            celda = image[y1:y2, x1:x2]

            if es_celda_vacia(celda):
                tipo_icono = 0  # vacio
            else:
                tipo_icono = detectar_icono(celda) or 0  # por si falla
            fila.append(tipo_icono)
        matriz_resultado.append(fila)
    # Matriz de signos horizontales (entre columnas)
    matriz_signos_h = []
    for i in range(rows):
        fila_signos = []
        for j in range(cols - 1):
            # Recorte centrado y cuadrado para el signo horizontal
            y1 = i * cell_h + int(cell_h * 0.35)
            y2 = (i + 1) * cell_h - int(cell_h * 0.35)
            x_centro = (j + 1) * cell_w
            ancho = int(cell_w * 0.4)
            x1 = x_centro - ancho // 2
            x2 = x_centro + ancho // 2
            franja = image[y1:y2, x1:x2]

            # # Debug visual
            # if i==3 and j==0:
            # cv2.imshow(f"Franja H [{i},{j}]", franja)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            

            signo = None
            if 4 in templates and detectar_signo(franja, templates[4], 0.5):
                signo = "="
            elif 3 in templates and detectar_signo(franja, templates[3], 0.4):
                signo = "x"
            fila_signos.append(signo)
        matriz_signos_h.append(fila_signos)

    # Matriz de signos verticales (entre filas)
    matriz_signos_v = []
    for i in range(rows - 1):
        fila_signos = []
        for j in range(cols):
            # Recorte centrado y cuadrado para el signo vertical
            x1 = j * cell_w + int(cell_w * 0.3)
            x2 = (j + 1) * cell_w - int(cell_w * 0.3)
            y_centro = (i + 1) * cell_h
            alto = int(cell_h * 0.3)
            y1 = y_centro - alto // 2
            y2 = y_centro + alto // 2
            franja = image[y1:y2, x1:x2]

            # # Debug visual
            # if i==2 and j==4:
            #     cv2.imshow(f"Franja H [{i},{j}]", franja)
            #     cv2.waitKey(0)
            #     cv2.destroyAllWindows()

            signo = None
            if 4 in templates and detectar_signo(franja, templates[4], 0.5):
                signo = "="
            elif 3 in templates and detectar_signo(franja, templates[3], 0.5):
                signo = "x"
            fila_signos.append(signo)
        matriz_signos_v.append(fila_signos)

    print("Matriz de iconos:")
    for fila in matriz_resultado:
        print(fila)
    print("Matriz de signos horizontales:")
    for fila in matriz_signos_h:
        print(fila)
    print("Matriz de signos verticales:")
    for fila in matriz_signos_v:
        print(fila)





if __name__ == '__main__':
    main()