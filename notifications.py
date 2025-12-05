import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class NotificationService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_from = os.getenv('EMAIL_FROM')
        
    def send_email(self, to_email, subject, html_content):
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_from
            msg['To'] = to_email
            
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Error enviando email: {e}")
            return False
    

    
    def send_booking_confirmation(self, booking):
        customer = booking['customer']
        print(f"\nEnviando confirmación por email a {customer['nombre']}")
        
        # Email de confirmación
        email_subject = f"Reserva confirmada - {booking['service_name']}"
        email_html = self.get_email_template(booking)
        
        email_sent = self.send_email(customer['email'], email_subject, email_html)
        print(f"Email enviado: {email_sent}")
        
        return {
            'email_sent': email_sent
        }
    
    def get_email_template(self, booking):
        customer = booking['customer']
        date_formatted = datetime.strptime(booking['date'], '%Y-%m-%d').strftime('%d/%m/%Y')
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #2c3e50, #e74c3c); color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 30px; }}
                .booking-details {{ background: #f8f9fa; border-radius: 8px; padding: 20px; margin: 20px 0; }}
                .detail-row {{ display: flex; justify-content: space-between; margin: 10px 0; }}
                .footer {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .btn {{ background: #e74c3c; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>¡Reserva Confirmada!</h1>
                    <p>Tu cita en Ferdistudio está confirmada</p>
                </div>
                
                <div class="content">
                    <h2>Hola {customer['nombre']},</h2>
                    <p>Tu reserva ha sido confirmada exitosamente. Aquí tienes todos los detalles:</p>
                    
                    <div class="booking-details">
                        <h3>Detalles de tu reserva</h3>
                        <div class="detail-row">
                            <strong>Servicio:</strong>
                            <span>{booking['service_name']}</span>
                        </div>
                        <div class="detail-row">
                            <strong>Fecha:</strong>
                            <span>{date_formatted}</span>
                        </div>
                        <div class="detail-row">
                            <strong>Hora:</strong>
                            <span>{booking['time']}</span>
                        </div>
                        <div class="detail-row">
                            <strong>Precio:</strong>
                            <span>${booking['price']:,}</span>
                        </div>
                        <div class="detail-row">
                            <strong>Profesional:</strong>
                            <span>Ferdi</span>
                        </div>
                    </div>
                    
                    <h3>Ubicación</h3>
                    <p>Av. Carabobo 27 6A<br>Buenos Aires, Comuna 7, Argentina</p>
                    
                    <h3>Contacto</h3>
                    <p>Teléfono: +541126510077</p>
                    
                    <p><strong>Importante:</strong> Te enviaremos un recordatorio 24 horas antes de tu cita.</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://wa.me/541126510077" class="btn">Contactar por WhatsApp</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Gracias por elegir Ferdistudio</p>
                    <p>¡Te esperamos!</p>
                </div>
            </div>
        </body>
        </html>
        """
    
