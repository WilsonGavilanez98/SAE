import face_recognition
import os

def registrar_estudiantes(carpeta):
    encodings = {}
    for filename in os.listdir(carpeta):
        if filename.lower().endswith((".jpg", ".png")):
            path = os.path.join(carpeta, filename)
            image = face_recognition.load_image_file(path)
            rostros = face_recognition.face_encodings(image)
            if rostros:
                nombre = os.path.splitext(filename)[0]
                encodings[nombre] = rostros[0]
                print(f"✅ Registrado: {nombre}")
            else:
                print(f"⚠️ No se detectó rostro en {filename}")
    return encodings