# Database.py
import psycopg2
from datetime import datetime

def get_connection():
    return psycopg2.connect(
        host="c9srcab37moub2.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
        database="dc0tv34qmb4d30",
        user="u8gijjt755tuos",
        password="p1115078641aa9e1d0e34aefcbe5828c7d3771a171c6dcf200a1c426c6898b69a"
    )

def guardar_resultado(id_matricula, id_emocion, probabilidad):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO resultado (id_matricula, id_emocion, fecha, probabilidad)
            VALUES (%s, %s, %s, %s)
        """
        ahora = datetime.now()
        valores = (id_matricula, id_emocion, ahora, probabilidad)

        cursor.execute(query, valores)
        conn.commit()
        print(f"✅ Resultado guardado → Matrícula: {id_matricula}, Emoción: {id_emocion}, Prob: {probabilidad:.2f}")

    except Exception as e:
        print("❌ ERROR al guardar en BD:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()

def obtener_id_emocion(nombre_emocion):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT id_emocion FROM emociones WHERE UPPER(nombre) = UPPER(%s)"
        cursor.execute(query, (nombre_emocion,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    finally:
        cursor.close()
        conn.close()


def obtener_id_estudiante_por_nombre(nombre_completo):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT id_estudiantes
            FROM estudiantes
            WHERE CONCAT(nombres, ' ', apellidos) = %s
            LIMIT 1
        """
        cursor.execute(query, (nombre_completo,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    finally:
        cursor.close()
        conn.close()

def obtener_ultima_matricula(id_estudiante):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT id_matricula
            FROM matricula
            WHERE id_estudiante = %s
            ORDER BY id_matricula DESC
            LIMIT 1
        """
        cursor.execute(query, (id_estudiante,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    finally:
        cursor.close()
        conn.close()

