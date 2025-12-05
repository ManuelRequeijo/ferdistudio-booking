import json
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from notifications import NotificationService

load_dotenv()

class ReminderService:
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
    
    def send_24h_reminder(self, booking):
        """Envía recordatorio 24h antes con opción de confirmación"""
        customer = booking['customer']
        
        # Verificar si es reserva de último minuto
        is_last_minute = booking.get('is_last_minute', False)
        
        if is_last_minute:
            # Mensaje para reservas de último minuto
            message = f"""Hola {customer['nombre']}! Confirmamos tu reserva:

{booking['date']} a las {booking['time']}
{booking['service_name']} - ${booking['price']:,}
Av. Carabobo 276A, Buenos Aires

Reserva de ultimo minuto confirmada
Te esperamos!

- Ferdistudio"""
        else:
            # Mensaje normal 24h antes
            message = f"""Hola {customer['nombre']}! Te recordamos tu cita manana:

{booking['date']} a las {booking['time']}
{booking['service_name']} - ${booking['price']:,}
Av. Carabobo 276A, Buenos Aires

Confirmas tu asistencia?
Responde:
SI para confirmar
NO para cancelar

Gracias! - Ferdistudio"""
        
        # Enviar WhatsApp
        success = self.send_whatsapp(customer['telefono'], message)
        
        if success:
            reminder_type = "último minuto" if is_last_minute else "24h"
            print(f"Recordatorio {reminder_type} enviado a {customer['nombre']}")
            return True
        else:
            reminder_type = "último minuto" if is_last_minute else "24h"
            print(f"Error enviando recordatorio {reminder_type} a {customer['nombre']}")
            return False
    
    def send_2h_reminder(self, booking):
        """Envía recordatorio 2h antes (solo si confirmó)"""
        customer = booking['customer']
        
        # Solo enviar si el cliente confirmó o si no hemos enviado el de 24h
        if not booking.get('confirmed_by_client', False) and booking['reminders']['24h']['sent']:
            print(f"Cliente {customer['nombre']} no confirmo, saltando recordatorio 2h")
            return False
        
        message = f"""Tu cita es en 2 horas!

Hoy {booking['time']} - {booking['service_name']}
Av. Carabobo 276A, Buenos Aires

Te esperamos!
- Ferdistudio"""
        
        success = self.send_whatsapp(customer['telefono'], message)
        
        if success:
            print(f"Recordatorio 2h enviado a {customer['nombre']}")
            return True
        else:
            print(f"Error enviando recordatorio 2h a {customer['nombre']}")
            return False
    
    def send_whatsapp(self, phone, message):
        """Envía mensaje de WhatsApp usando CallMeBot"""
        try:
            api_key = os.getenv('WHATSAPP_API_KEY')
            if not api_key:
                print("WHATSAPP_API_KEY no configurado")
                return False
            
            # Limpiar número
            phone_clean = phone.replace('+', '').replace(' ', '').replace('-', '')
            
            # URL de CallMeBot
            api_url = "https://api.callmebot.com/whatsapp.php"
            params = {
                'phone': phone_clean,
                'text': message,
                'apikey': api_key
            }
            
            response = requests.get(api_url, params=params, timeout=10)
            
            if response.status_code == 200 and 'Message queued' in response.text:
                return True
            else:
                print(f"Error WhatsApp: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error enviando WhatsApp: {e}")
            return False
    
    def check_and_send_reminders(self):
        """Verifica y envía recordatorios pendientes"""
        print(f"\nVerificando recordatorios - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        bookings = self.load_bookings()
        updated = False
        sent_count = 0
        
        now = datetime.now()
        
        for booking in bookings:
            # Solo procesar reservas futuras
            booking_datetime = datetime.strptime(f"{booking['date']} {booking['time']}", '%Y-%m-%d %H:%M')
            if booking_datetime <= now:
                continue
            
            # Verificar recordatorio 24h
            if not booking['reminders']['24h']['sent']:
                scheduled_24h = datetime.fromisoformat(booking['reminders']['24h']['scheduled_for'])
                if now >= scheduled_24h:
                    is_last_minute = booking.get('is_last_minute', False)
                    reminder_type = "de último minuto" if is_last_minute else "24h"
                    print(f"Enviando recordatorio {reminder_type} a {booking['customer']['nombre']}...")
                    
                    if self.send_24h_reminder(booking):
                        booking['reminders']['24h']['sent'] = True
                        booking['reminders']['24h']['sent_at'] = now.isoformat()
                        updated = True
                        sent_count += 1
            
            # Verificar recordatorio 2h (solo si no fue saltado)
            if not booking['reminders']['2h']['sent'] and not booking['reminders']['2h'].get('skipped_reason'):
                scheduled_2h = datetime.fromisoformat(booking['reminders']['2h']['scheduled_for'])
                if now >= scheduled_2h:
                    print(f"Enviando recordatorio 2h a {booking['customer']['nombre']}...")
                    
                    if self.send_2h_reminder(booking):
                        booking['reminders']['2h']['sent'] = True
                        booking['reminders']['2h']['sent_at'] = now.isoformat()
                        updated = True
                        sent_count += 1
        
        if updated:
            self.save_bookings(bookings)
            print(f"{sent_count} recordatorios enviados y actualizados")
        else:
            print("No hay recordatorios pendientes")
    
    def mark_client_confirmation(self, booking_id, confirmed=True):
        """Marca la confirmación del cliente"""
        bookings = self.load_bookings()
        
        for booking in bookings:
            if booking['id'] == booking_id:
                booking['confirmed_by_client'] = confirmed
                booking['confirmation_date'] = datetime.now().isoformat()
                self.save_bookings(bookings)
                return True
        
        return False

if __name__ == "__main__":
    reminder_service = ReminderService()
    reminder_service.check_and_send_reminders()