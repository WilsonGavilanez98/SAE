# Database.py
import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
from datetime import datetime

# Ruta absoluta al archivo credenciales.env
dotenv_path = Path(__file__).resolve().parent / "credenciales.env"
load_dotenv(dotenv_path=dotenv_path)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
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

def obtener_estudiantes_alerta():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
       WITH RESUMEN AS (SELECT 
                        R.ID_MATRICULA,
                        CONCAT(MA.APELLIDOS,' ',MA.NOMBRES) AS ESTUDIANTE,
                        E.NOMBRE AS EMOCION,
                        U.ID_PROFESOR,
                        MAX(DATE(R.FECHA)) AS ULTIMA_FECHA,
                        COUNT(DISTINCT DATE(R.FECHA)) AS DIAS
                    FROM 
                        RESULTADO R
                    JOIN
                        MATRICULA U ON R.ID_MATRICULA = U.ID_MATRICULA
                    JOIN 
                        ESTUDIANTES MA ON R.ID_MATRICULA = MA.ID_ESTUDIANTES
                    JOIN 
                        EMOCIONES E ON R.ID_EMOCION = E.ID_EMOCION
                    WHERE UPPER
                        (E.NOMBRE) IN ('TRISTE', 'ENOJADO', 'MIEDO')
                    GROUP BY
                        R.ID_MATRICULA,
                        MA.APELLIDOS,
                        MA.NOMBRES,
                        E.NOMBRE,
                        U.ID_PROFESOR
                    ORDER BY 
                        CONCAT(MA.APELLIDOS,' ',MA.NOMBRES)
                    )
                    SELECT 
                            R.ID_MATRICULA,
                            R.ESTUDIANTE,
                            R.EMOCION,
                            PO.EMAIL,
                            R.ULTIMA_FECHA,
                            R.DIAS
                            FROM RESUMEN R
                            JOIN 
                                PROFESORES PO ON R.ID_PROFESOR = PO.ID_PROFESOR
                            WHERE r.DIAS >= 3
                            AND NOT EXISTS (
                                SELECT 1 FROM alertas_enviadas ae
                                WHERE ae.id_matricula = r.id_matricula
                                AND ae.id_emocion = (SELECT id_emocion FROM emociones WHERE nombre = r.EMOCION)
                                AND ae.ultima_fecha >= r.ultima_fecha
    )"""
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


def registrar_alerta(id_matricula, emocion, fecha):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO alertas_enviadas (id_matricula, id_emocion, ultima_fecha)
        VALUES (%s, (SELECT id_emocion FROM emociones WHERE nombre = %s), %s)
    """

    cursor.execute(query, (id_matricula, emocion, fecha))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_estudiantes_con_fotos():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT CONCAT(nombres, ' ', apellidos) AS nombre_completo, foto
        FROM estudiantes
        WHERE foto IS NOT NULL
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


