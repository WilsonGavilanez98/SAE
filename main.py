from Reconocimiento import capturar_y_reconocer
from Estudiantes import registrar_estudiantes_desde_urls
from Database import obtener_estudiantes_con_fotos
from Config import intervalo_segundos

# Obtener lista de (nombre completo, url_foto) desde la base de datos
estudiantes_urls = obtener_estudiantes_con_fotos()

# Cargar encodings desde las imágenes en Cloudinary
students_encodings = registrar_estudiantes_desde_urls(estudiantes_urls)

# Iniciar reconocimiento facial + emociones
capturar_y_reconocer(students_encodings, intervalo_segundos)
