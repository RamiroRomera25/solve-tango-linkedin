import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder = "dark"
folderSigns = "signs"
TEMPLATE_PATH = os.path.join(BASE_DIR, "images", folder)
ENTRADA_PATH = os.path.join(BASE_DIR, "images", "template_dark.PNG")
SIGN_PATH = os.path.join(BASE_DIR, "images", folderSigns)

# Cargar templates - agregamos multiply (x) y equal (=)
templates = {
    0: cv2.imread(os.path.join(TEMPLATE_PATH, "empty.PNG"), cv2.IMREAD_COLOR),
    1: cv2.imread(os.path.join(TEMPLATE_PATH, "sol.PNG"), cv2.IMREAD_COLOR),
    2: cv2.imread(os.path.join(TEMPLATE_PATH, "luna.PNG"), cv2.IMREAD_COLOR),
    3: cv2.imread(os.path.join(SIGN_PATH, "multiply.PNG"), cv2.IMREAD_COLOR),  # símbolo 'x'
    4: cv2.imread(os.path.join(SIGN_PATH, "equal.PNG"), cv2.IMREAD_COLOR),     # símbolo '='
}

# Verificar templates cargados
for key, tpl in templates.items():
    if tpl is None:
        print(f"❌ Template {key} no se pudo cargar")
        exit(1)
    else:
        print(f"✅ Template {key} cargado correctamente")

image = cv2.imread(ENTRADA_PATH, cv2.IMREAD_COLOR)
if image is None:
    print("❌ Imagen principal no se pudo cargar")
    exit(1)

rows, cols = 6, 6
cell_h = image.shape[0] // rows
cell_w = image.shape[1] // cols

def es_celda_vacia(celda, umbral=0.7):
    """Detecta si una celda está vacía"""
    template = templates[0]
    template_resized = cv2.resize(template, (celda.shape[1], celda.shape[0]))
    
    # Convertir ambos a escala de grises para mejor comparación
    celda_gray = cv2.cvtColor(celda, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_resized, cv2.COLOR_BGR2GRAY)
    
    res = cv2.matchTemplate(celda_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, score, _, _ = cv2.minMaxLoc(res)
    
    return score >= umbral

def detectar_icono(celda, umbral=0.5):
    """Detecta qué tipo de icono hay en la celda"""
    # Recorta el centro para mejorar la detección
    h, w = celda.shape[:2]
    offset = int(min(h, w) * 0.15)  # Reducimos el offset para símbolos más pequeños
    celda_recortada = celda[offset:h - offset, offset:w - offset]

    max_score = -1
    mejor_id = None
    scores_debug = {}

    # Probamos con todos los templates excepto el vacío (0)
    for tipo_id in [1, 2, 3, 4]:  # sol, luna, multiply, equal
        template = templates[tipo_id]
        
        # Recortamos el template también
        tpl_recortado = template[offset:template.shape[0]-offset, offset:template.shape[1]-offset]
        tpl_resized = cv2.resize(tpl_recortado, (celda_recortada.shape[1], celda_recortada.shape[0]))

        # Probamos tanto en color como en escala de grises
        # Método 1: Comparación en color
        res_color = cv2.matchTemplate(celda_recortada, tpl_resized, cv2.TM_CCOEFF_NORMED)
        _, score_color, _, _ = cv2.minMaxLoc(res_color)
        
        # Método 2: Comparación en escala de grises
        celda_gray = cv2.cvtColor(celda_recortada, cv2.COLOR_BGR2GRAY)
        tpl_gray = cv2.cvtColor(tpl_resized, cv2.COLOR_BGR2GRAY)
        res_gray = cv2.matchTemplate(celda_gray, tpl_gray, cv2.TM_CCOEFF_NORMED)
        _, score_gray, _, _ = cv2.minMaxLoc(res_gray)
        
        # Tomamos el mejor score de ambos métodos
        score = max(score_color, score_gray)
        scores_debug[tipo_id] = score

        if score > max_score:
            max_score = score
            mejor_id = tipo_id

    # Debug: mostrar todos los scores
    simbolos = {0: "vacío", 1: "sol", 2: "luna", 3: "x", 4: "="}
    print(f"Scores: {[(simbolos[k], f'{v:.3f}') for k, v in scores_debug.items()]}")
    print(f"Mejor match: {simbolos.get(mejor_id, 'desconocido')} con score {max_score:.3f}")

    return mejor_id if max_score >= umbral else None

def detectar_simbolos_alternativos(celda):
    """Método alternativo para detectar símbolos basado en características de la imagen"""
    # Convertir a escala de grises
    gray = cv2.cvtColor(celda, cv2.COLOR_BGR2GRAY)
    
    # Aplicar threshold para obtener imagen binaria
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Encontrar contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return 0  # vacío
    
    # Análisis de contornos para identificar símbolos
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 50:  # muy pequeño, probablemente ruido
            continue
            
        # Calcular bounding box
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h
        
        # Heurísticas para identificar símbolos
        if 0.8 < aspect_ratio < 1.2:  # aproximadamente cuadrado
            # Podría ser 'x' o símbolo circular
            pass
        elif aspect_ratio > 2:  # muy horizontal
            # Podría ser '='
            return 4
    
    return None

matriz_resultado = []

def main():
    print("🔍 Iniciando procesamiento de imagen...")
    print(f"Dimensiones de imagen: {image.shape}")
    print(f"Dimensiones de celda: {cell_w}x{cell_h}")
    
    for i in range(rows):
        fila = []
        for j in range(cols):
            y1, y2 = i * cell_h, (i + 1) * cell_h
            x1, x2 = j * cell_w, (j + 1) * cell_w
            celda = image[y1:y2, x1:x2]

            print(f"\n--- Procesando celda ({i},{j}) ---")
            
            # Primero verificamos si está vacía
            if es_celda_vacia(celda, umbral=0.7):
                tipo_icono = 0
                print("✅ Celda vacía detectada")
            else:
                # Intentamos detectar el icono
                tipo_icono = detectar_icono(celda, umbral=0.4)  # Bajamos el umbral
                
                # Si no se detecta nada, intentamos método alternativo
                if tipo_icono is None:
                    print("⚠️ No se detectó con template matching, probando método alternativo...")
                    tipo_icono = detectar_simbolos_alternativos(celda)
                
                # Si aún no se detecta nada, asumimos vacío
                if tipo_icono is None:
                    tipo_icono = 0
                    print("❓ No se pudo identificar, asumiendo vacío")
                
                simbolos = {0: "vacío", 1: "sol", 2: "luna", 3: "x", 4: "="}
                print(f"✅ Detectado: {simbolos[tipo_icono]}")
            
            fila.append(tipo_icono)
        matriz_resultado.append(fila)
    
    print("\n" + "="*50)
    print("RESULTADO FINAL:")
    print("="*50)
    
    simbolos = {0: "⬜", 1: "☀️", 2: "🌙", 3: "❌", 4: "➖"}
    
    for i, fila in enumerate(matriz_resultado):
        fila_simbolos = [simbolos.get(x, str(x)) for x in fila]
        print(f"Fila {i}: {fila}")
        print(f"      {' '.join(fila_simbolos)}")
    
    print(f"\nMatriz numérica completa:")
    print(matriz_resultado)

if __name__ == '__main__':
    main()