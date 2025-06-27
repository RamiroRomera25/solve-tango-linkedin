import pyautogui
import time
from datetime import datetime

# Configuración
pyautogui.FAILSAFE = True  # Mover mouse a esquina superior izquierda para cancelar


def captura_rapida():
    """Captura rápida del área central de la pantalla donde está el juego"""

    print("🎮 Capturando juego Tango en 3 segundos...")
    print("💡 Asegúrate de que el juego esté visible en LinkedIn")

    # Countdown
    for i in range(3, 0, -1):
        print(f"⏰ {i}...")
        time.sleep(1)

    # Obtener dimensiones de pantalla
    width, height = pyautogui.size()
    print(f"H: {height} | W: {width}")

    # Coordenadas para capturar el área del juego
    # Ajusta estos valores según tu pantalla y posición del juego
    x = width // 2 - 205  # Centro horizontal
    y = height // 2 - 313  # Centro vertical
    w = 396  # Ancho de captura
    h = 394  # Alto de captura

    # Capturar
    screenshot = pyautogui.screenshot(region=(x, y, w, h))

    # Guardar con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tango.png"
    screenshot.save(filename)

    print(f"✅ ¡Captura guardada como {filename}!")
    print(f"📍 Área capturada: {x}, {y} ({w}x{h})")


if __name__ == "__main__":
    captura_rapida()