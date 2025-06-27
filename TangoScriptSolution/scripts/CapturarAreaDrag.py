import cv2
import numpy as np
import pyautogui

start_point = None
end_point = None
drawing = False
region_seleccionada = None

def seleccionar_area_con_drag():
    global start_point, end_point, drawing, region_seleccionada

    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    clone = screenshot.copy()

    def mouse_callback(event, x, y, flags, param):
        nonlocal screenshot
        global start_point, end_point, drawing

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            start_point = (x, y)

        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            screenshot = clone.copy()
            cv2.rectangle(screenshot, start_point, (x, y), (0, 255, 0), 2)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            end_point = (x, y)
            cv2.rectangle(screenshot, start_point, end_point, (0, 255, 0), 2)

    cv2.namedWindow("Seleccioná el área")
    cv2.setMouseCallback("Seleccioná el área", mouse_callback)

    while True:
        cv2.imshow("Seleccioná el área", screenshot)
        key = cv2.waitKey(1) & 0xFF
        if key in [13, 27]:  # Enter o Esc
            break

    cv2.destroyAllWindows()

    if start_point and end_point:
        x1, y1 = start_point
        x2, y2 = end_point
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        region_seleccionada = {"left": left, "top": top, "width": width, "height": height}
        return region_seleccionada
    else:
        print("❌ No se seleccionó ninguna región")
        return None

def capturar_region(region):
    # Usa pyautogui que es más preciso en sistemas con escalado
    screenshot = pyautogui.screenshot(region=(region["left"], region["top"], region["width"], region["height"]))
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# Prueba
if __name__ == "__main__":
    region = seleccionar_area_con_drag()
    if region:
        print("🟢 Región seleccionada:", region)
        # Cierra la ventana de selección antes de capturar
        cv2.destroyAllWindows()
        imagen = capturar_region(region)
        cv2.imwrite("captura_temp.png", imagen)
        cv2.imshow("Imagen capturada", imagen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
