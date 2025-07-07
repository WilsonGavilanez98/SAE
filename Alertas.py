import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Database import obtener_estudiantes_alerta, registrar_alerta

# === CONFIGURACIÓN ===
EMAIL_FROM = "arielposligua89@gmail.com"
EMAIL_PASSWORD = "fbgv cepr bsgy wcgn"  # Contraseña de aplicación de Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# === ENVÍO DE CORREO ===
def enviar_correo(destinatario, asunto, mensaje_html):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = destinatario
    msg["Subject"] = asunto

    msg.attach(MIMEText(mensaje_html, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"📧 Correo enviado a {destinatario}")
    except Exception as e:
        print(f"❌ Error al enviar correo a {destinatario}: {e}")

# === MENSAJE FORMATEADO EN HTML ===
def generar_mensaje_html(estudiante, emocion, dias):
    return f"""\
    <html>
        <body>
            <p>Estimado/a docente,</p>

            <p>Le informamos que el estudiante <strong>{estudiante}</strong> ha mostrado indicios de la emoción 
            <strong>'{emocion}'</strong> en al menos <strong>{dias} días diferentes</strong>.</p>

            <p>Este patrón podría ser indicativo de un estado emocional persistente. Le sugerimos prestar atención a su comportamiento y, de ser necesario, considerar una orientación adicional.</p>

            <p>Atentamente,<br>
            <em>El sistema de monitoreo emocional estudiantil</em></p>
        </body>
    </html>
    """

# === PROCESAMIENTO DE ALERTAS REALES ===
def verificar_alertas():
    resultados = obtener_estudiantes_alerta()

    for id_matricula, estudiante, emocion, email, ultima_fecha, dias in resultados:
        mensaje_html = generar_mensaje_html(estudiante, emocion, dias)
        asunto = f"Alerta emocional: {estudiante}"
        enviar_correo(email, asunto, mensaje_html)
        registrar_alerta(id_matricula, emocion, ultima_fecha)

# === MODO DE PRUEBA: ENVÍA UN CORREO CON DATOS FALSOS ===
def prueba_envio_oficial():
    estudiante = "Juan Pérez"
    emocion = "tristeza"
    dias = 4
    email_destino = "wilsongavilanez732@gmail.com"  # ⚠️ Cambia esto por tu correo personal

    mensaje_html = generar_mensaje_html(estudiante, emocion, dias)
    asunto = f"Alerta emocional: {estudiante} (PRUEBA)"
    enviar_correo(email_destino, asunto, mensaje_html)

# === PUNTO DE ENTRADA ===
if __name__ == "__main__":
    # Descomenta la opción que necesites

    #Ejecución normal con base de datos real
    verificar_alertas()

    # 🧪 Envío de prueba con datos falsos al correo personal
    # prueba_envio_oficial()
