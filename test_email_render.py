"""
Test para verificar que el email funciona con las mismas configuraciones de Render
"""
import os
from dotenv import load_dotenv
from notifications import NotificationService

load_dotenv()

def test_email():
    print("=== TEST EMAIL RENDER ===")
    
    # Mostrar configuración
    print(f"SMTP_SERVER: {os.getenv('SMTP_SERVER')}")
    print(f"SMTP_PORT: {os.getenv('SMTP_PORT')}")
    print(f"EMAIL_USER: {os.getenv('EMAIL_USER')}")
    print(f"EMAIL_FROM: {os.getenv('EMAIL_FROM')}")
    
    # Test booking fake
    fake_booking = {
        'id': 999,
        'service_name': 'Test Corte',
        'price': 20000,
        'date': '2025-12-06',
        'time': '15:00',
        'customer': {
            'nombre': 'Test',
            'apellido': 'Usuario',
            'email': 'manuel.requeijo2006@gmail.com'  # Tu email para test
        }
    }
    
    try:
        notification_service = NotificationService()
        result = notification_service.send_booking_confirmation(fake_booking)
        
        if result['email_sent']:
            print("✅ EMAIL ENVIADO CORRECTAMENTE")
        else:
            print("❌ ERROR ENVIANDO EMAIL")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_email()