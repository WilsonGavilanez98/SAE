import cv2
import face_recognition
import numpy as np
import time
from Config import rtsp_url
from Emociones import predecir_emocion
from Database import (
    guardar_resultado,
    obtener_id_emocion,
    obtener_id_estudiante_por_nombre,
    obtener_ultima_matricula
)

def capturar_y_reconocer(estudiantes, intervalo):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("❌ No se pudo abrir el stream.")
        return

    tiempo_ultima_captura = time.time()
    rostros_actuales = []
    ultimo_guardado_por_estudiante = {}  # ⏱️ Control por estudiante

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ No se pudo leer el frame.")
            break

        if time.time() - tiempo_ultima_captura >= intervalo:
            tiempo_ultima_captura = time.time()
            rostros_actuales = []

            pequeño = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb = cv2.cvtColor(pequeño, cv2.COLOR_BGR2RGB)

            ubicaciones = face_recognition.face_locations(rgb)
            codigos = face_recognition.face_encodings(rgb, ubicaciones)

            for (top, right, bottom, left), cod in zip(ubicaciones, codigos):
                nombre = "Desconocido"
                if estudiantes:
                    distancias = face_recognition.face_distance(list(estudiantes.values()), cod)
                    mejor_match = np.argmin(distancias)
                    if distancias[mejor_match] < 0.6:
                        nombre = list(estudiantes.keys())[mejor_match]

                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                rostro = frame[top:bottom, left:right]
                emocion = "?"
                probabilidad = 0.0

                if rostro.size > 0:
                    gris = cv2.cvtColor(rostro, cv2.COLOR_BGR2GRAY)
                    try:
                        emocion, probabilidad = predecir_emocion(gris)
                        print(f"🎯 Emoción detectada (modelo): '{emocion}'")
                    except Exception as e:
                        print("❌ ERROR al predecir emoción:", e)
                        continue

                    if nombre != "Desconocido":
                        print("✅ Estudiante reconocido:", nombre)
                        id_estudiante = obtener_id_estudiante_por_nombre(nombre)
                        print("ID estudiante:", id_estudiante)
                        id_matricula = obtener_ultima_matricula(id_estudiante) if id_estudiante else None
                        print("ID matrícula:", id_matricula)
                        id_emocion = obtener_id_emocion(emocion)
                        print("ID emoción:", id_emocion)

                        if id_matricula and id_emocion:
                            clave = f"{id_matricula}"
                            ahora = time.time()
                            ultimo_guardado = ultimo_guardado_por_estudiante.get(clave, 0)

                            if ahora - ultimo_guardado >= intervalo:
                                print(f"📝 Guardando para {nombre} (intervalo cumplido)")
                                guardar_resultado(id_matricula, id_emocion, probabilidad)
                                ultimo_guardado_por_estudiante[clave] = ahora
                            else:
                                print(f"⏱️ Esperando para {nombre} (aún no pasan {intervalo}s)")

                rostros_actuales.append((f"{nombre}: {emocion}", (top, right, bottom, left)))

        for texto, (top, right, bottom, left) in rostros_actuales:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, texto, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Reconocimiento Facial + Emocion", frame)
        cv2.resizeWindow("Reconocimiento Facial + Emocion", 1000, 800)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
