import face_recognition
import requests
import numpy as np
from PIL import Image
import io

def registrar_estudiantes_desde_urls(lista_estudiantes):
    encodings = {}

    for nombre, url in lista_estudiantes:
        try:
            print(f"🔄 Descargando imagen de: {nombre}")
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content)).convert('RGB')
            image_np = np.array(image)

            rostros = face_recognition.face_encodings(image_np)
            if rostros:
                encodings[nombre] = rostros[0]
                print(f"✅ Registrado: {nombre}")
            else:
                print(f"⚠️ No se detectó rostro en la imagen de {nombre}")
        except Exception as e:
            print(f"❌ Error con {nombre}: {e}")

    return encodings
