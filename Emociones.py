from tensorflow.keras.models import load_model # type: ignore
import numpy as np
from Config import modelo_path, EMOCIONES
import cv2

modelo_emociones = load_model(modelo_path)

def predecir_emocion(rostro_gris):
    redim = cv2.resize(rostro_gris, (48, 48))
    input_modelo = redim.reshape(1, 48, 48, 1) / 255.0
    prediccion = modelo_emociones.predict(input_modelo, verbose=0)
    indice = np.argmax(prediccion)
    emocion = EMOCIONES[indice]
    probabilidad = float(prediccion[0][indice])
    return emocion, probabilidad

