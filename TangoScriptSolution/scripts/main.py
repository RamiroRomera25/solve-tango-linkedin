from CapturarImagen import captura_rapida
import ProcesarImagen

if __name__ == "__main__":
    # Captura el área del juego y guarda la imagen como "tango.png"
    captura_rapida()  # Esta función debe guardar la imagen como "tango.png"

    # Procesa la imagen capturada
    ProcesarImagen.ENTRADA_PATH = "tango.png"
    ProcesarImagen.main()