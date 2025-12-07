import json
import os
from datetime import datetime
from notifications import NotificationService

class EmailReminderService:
    def __init__(self):
        self.bookings_file = 'data/bookings.json'
        self.notification_service = NotificationService()
        
    def load_bookings(self):
        if os.path.exists(self.bookings_file):
            with open(self.bookings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_bookings(self, bookings):
        with open(self.bookings_file, 'w', encoding='utf-8') as f:
            json.dump(bookings, f, ensure_ascii=False, indent=2)
    
    def send_reminder_email(self, booking):
        """Envía recordatorio por email 24h antes"""
        customer = booking['customer']
        date_formatted = datetime.strptime(booking['date'], '%Y-%m-%d').strftime('%d/%m/%Y')
        
        subject = f"Recordatorio: Tu cita mañana en Ferdistudio"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #2c3e50, #e74c3c); color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 30px; }}
                .reminder-box {{ background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 20px; margin: 20px 0; }}
                .booking-details {{ background: #f8f9fa; border-radius: 8px; padding: 20px; margin: 20px 0; }}
                .detail-row {{ display: flex; justify-content: space-between; margin: 10px 0; }}
                .footer {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .btn {{ background: #e74c3c; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>¡Tu cita es mañana!</h1>
                    <p>Recordatorio de tu reserva en Ferdistudio</p>
                </div>
                
                <div class="content">
                    <div class="reminder-box">
                        <h3>🕐 Recordatorio importante</h3>
                        <p><strong>Tu cita es mañana {date_formatted} a las {booking['time']}</strong></p>
                        <p>Te esperamos en Av. Carabobo 276A, Buenos Aires</p>
                    </div>
                    
                    <h2>Hola {customer['nombre']},</h2>
                    <p>Este es un recordatorio amigable de que tienes una cita programada para mañana.</p>
                    
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
                            <strong>Profesional:</strong>
                            <span>Ferdi</span>
                        </div>
                    </div>
                    
                    <h3>Recomendaciones</h3>
                    <ul>
                        <li>Llega 5 minutos antes de tu cita</li>
                        <li>Si necesitas cancelar o reprogramar, contáctanos cuanto antes</li>
                        <li>Trae una referencia si tienes un corte específico en mente</li>
                    </ul>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://wa.me/541126510077" class="btn">Contactar por WhatsApp</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>¡Te esperamos mañana!</p>
                    <p>Ferdistudio - Av. Carabobo 276A, Buenos Aires</p>
                    <p>Tel: +541126510077</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.notification_service.send_email(customer['email'], subject, html_content)
    
    def check_and_send_reminders(self):
        """Verifica y envía recordatorios por email pendientes"""
        print(f"Verificando recordatorios por email - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        bookings = self.load_bookings()
        updated = False
        sent_count = 0
        
        now = datetime.now()
        
        for booking in bookings:
            # Solo procesar reservas futuras que tengan estructura de email_reminder
            if 'email_reminder' not in booking:
                continue
                
            booking_datetime = datetime.strptime(f"{booking['date']} {booking['time']}", '%Y-%m-%d %H:%M')
            if booking_datetime <= now:
                continue
            
            # Verificar recordatorio por email
            if not booking['email_reminder']['sent']:
                scheduled_time = datetime.fromisoformat(booking['email_reminder']['scheduled_for'])
                if now >= scheduled_time:
                    print(f"Enviando recordatorio por email a {booking['customer']['nombre']}...")
                    
                    if self.send_reminder_email(booking):
                        booking['email_reminder']['sent'] = True
                        booking['email_reminder']['sent_at'] = now.isoformat()
                        updated = True
                        sent_count += 1
                        print(f"Recordatorio enviado a {booking['customer']['email']}")
                    else:
                        print(f"Error enviando recordatorio a {booking['customer']['email']}")
        
        if updated:
            self.save_bookings(bookings)
            print(f"{sent_count} recordatorios por email enviados")
        else:
            print("No hay recordatorios pendientes")

if __name__ == "__main__":
    reminder_service = EmailReminderService()
    reminder_service.check_and_send_reminders()