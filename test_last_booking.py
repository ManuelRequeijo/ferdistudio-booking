import json
import os
from notifications import NotificationService

def test_last_booking():
    print("=== PROBANDO NOTIFICACIONES DE ULTIMA RESERVA ===")
    
    # Cargar última reserva
    with open('data/bookings.json', 'r', encoding='utf-8') as f:
        bookings = json.load(f)
    
    last_booking = bookings[-1]
    print(f"Reserva ID: {last_booking['id']}")
    print(f"Cliente: {last_booking['customer']['nombre']}")
    print(f"Teléfono: {last_booking['customer']['telefono']}")
    
    # Probar notificaciones
    notification_service = NotificationService()
    result = notification_service.send_booking_confirmation(last_booking)
    
    print(f"\nResultados:")
    print(f"Email enviado: {result['email_sent']}")
    print(f"WhatsApp enviado: {result['whatsapp_sent']}")

if __name__ == "__main__":
    test_last_booking()