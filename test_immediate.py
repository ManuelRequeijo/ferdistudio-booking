#!/usr/bin/env python3
"""
Script para crear reserva con recordatorio inmediato
"""
import json
from datetime import datetime, timedelta
from reminder_service import ReminderService

def test_immediate():
    """Crea una reserva con recordatorio inmediato"""
    
    try:
        with open('data/bookings.json', 'r', encoding='utf-8') as f:
            bookings = json.load(f)
    except:
        bookings = []
    
    # Crear reserva para dentro de 3 horas
    future_time = datetime.now() + timedelta(hours=3)
    booking_date = future_time.strftime('%Y-%m-%d')
    booking_time = future_time.strftime('%H:%M')
    
    # Recordatorio inmediato
    reminder_now = datetime.now()
    
    test_booking = {
        'id': len(bookings) + 1,
        'service_id': 'corte',
        'service_name': 'Corte',
        'price': 20000,
        'duration': 30,
        'date': booking_date,
        'time': booking_time,
        'customer': {
            'nombre': 'Prueba',
            'apellido': 'Inmediata',
            'email': 'test@example.com',
            'telefono': '+541126510077',
            'observaciones': 'Prueba de recordatorio inmediato'
        },
        'status': 'confirmed',
        'created_at': datetime.now().isoformat(),
        'reminders': {
            '24h': {
                'sent': False,
                'scheduled_for': reminder_now.isoformat(),
                'type': 'confirmation'
            },
            '2h': {
                'sent': False,
                'scheduled_for': (future_time - timedelta(hours=2)).isoformat(),
                'type': 'final_reminder'
            }
        },
        'confirmed_by_client': False
    }
    
    bookings.append(test_booking)
    
    with open('data/bookings.json', 'w', encoding='utf-8') as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)
    
    print(f"Reserva inmediata creada:")
    print(f"   ID: {test_booking['id']}")
    print(f"   Recordatorio: AHORA")
    
    # Ejecutar recordatorios
    print(f"\nEjecutando verificacion...")
    reminder_service = ReminderService()
    reminder_service.check_and_send_reminders()

if __name__ == "__main__":
    test_immediate()