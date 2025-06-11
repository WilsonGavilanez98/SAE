from Reconocimiento import capturar_y_reconocer
from Estudiantes import registrar_estudiantes
from Config import carpeta_estudiantes, intervalo_segundos

# Cargar estudiantes registrados
students_encodings = registrar_estudiantes(carpeta_estudiantes)

# Iniciar reconocimiento facial + emociones
capturar_y_reconocer(students_encodings, intervalo_segundos)
