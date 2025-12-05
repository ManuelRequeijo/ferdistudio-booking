import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

def test_email():
    print("=== PRUEBA DE EMAIL ===")
    
    # Obtener configuración
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_from = os.getenv('EMAIL_FROM')
    
    print(f"SMTP Server: {smtp_server}")
    print(f"SMTP Port: {smtp_port}")
    print(f"Email User: {email_user}")
    print(f"Email From: {email_from}")
    print(f"Password configurada: {'Sí' if email_password else 'No'}")
    
    try:
        # Crear mensaje de prueba
        msg = MIMEMultipart()
        msg['Subject'] = "Prueba de Email - Ferdistudio"
        msg['From'] = email_from
        msg['To'] = email_user  # Enviamos a nosotros mismos
        
        html_content = """
        <h1>Prueba de Email</h1>
        <p>Si recibes este email, la configuración está funcionando correctamente.</p>
        """
        
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        print("\nConectando al servidor SMTP...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        print("Iniciando sesión...")
        server.login(email_user, email_password)
        
        print("Enviando email...")
        server.send_message(msg)
        server.quit()
        
        print("EMAIL ENVIADO EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_email()