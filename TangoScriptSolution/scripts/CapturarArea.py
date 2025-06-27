import mss
import numpy as np
import cv2
import pyautogui
import time

def seleccionar_area_con_mouse():
    print("Colocá el mouse en la esquina superior izquierda y esperá...")
    time.sleep(1)
    esquina_superior = pyautogui.position()
    print(f"🟢 Esquina superior: {esquina_superior}")

    print("Ahora colocá el mouse en la esquina inferior derecha y esperá...")
    time.sleep(2)
    esquina_inferior = pyautogui.position()
    print(f"🔵 Esquina inferior: {esquina_inferior}")

    region = {
        "left": min(esquina_superior.x, esquina_inferior.x),
        "top": min(esquina_superior.y, esquina_inferior.y),
        "width": abs(esquina_inferior.x - esquina_superior.x),
        "height": abs(esquina_inferior.y - esquina_superior.y)
    }

    return region
def capturar_area(region):
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
def click_en_relativo(region, rel_x, rel_y):
    # rel_x y rel_y son proporciones: 0.5 = centro, 0.25 = un cuarto
    abs_x = region["left"] + int(region["width"] * rel_x)
    abs_y = region["top"] + int(region["height"] * rel_y)
    pyautogui.click(x=abs_x, y=abs_y)
    abs_x = region["left"] + int(region["width"] * 0.25)
    abs_y = region["top"] + int(region["height"] * 0.25)
    pyautogui.rightClick(x=abs_x, y=abs_y)

if __name__ == "__main__":
    region = seleccionar_area_con_mouse()
    imagen = capturar_area(region)
    cv2.imwrite("captura_temp.png", imagen)
    # # Mostrar la imagen capturada
    cv2.imshow("Área seleccionada", imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

