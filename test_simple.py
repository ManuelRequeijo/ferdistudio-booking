#!/usr/bin/env python3
"""
Script simple para probar recordatorios sin emojis
"""
import json
from datetime import datetime, timedelta
from reminder_service import ReminderService

def create_test_booking():
    """Crea una reserva de prueba para manana"""
    
    try:
        with open('data/bookings.json', 'r', encoding='utf-8') as f:
            bookings = json.load(f)
    except:
        bookings = []
    
    # Crear reserva para manana a las 14:00
    tomorrow = datetime.now() + timedelta(days=1)
    booking_date = tomorrow.strftime('%Y-%m-%d')
    booking_time = "14:00"
    
    # Calcular recordatorios
    booking_datetime = datetime.strptime(f"{booking_date} {booking_time}", '%Y-%m-%d %H:%M')
    reminder_24h = booking_datetime - timedelta(hours=24)
    reminder_2h = booking_datetime - timedelta(hours=2)
    
    test_booking = {
        'id': len(bookings) + 1,
        'service_id': 'corte',
        'service_name': 'Corte',
        'price': 20000,
        'duration': 30,
        'date': booking_date,
        'time': booking_time,
        'customer': {
            'nombre': 'Test',
            'apellido': 'Usuario',
            'email': 'test@example.com',
            'telefono': '+541126510077',
            'observaciones': 'Reserva de prueba para recordatorios'
        },
        'status': 'confirmed',
        'created_at': datetime.now().isoformat(),
        'reminders': {
            '24h': {
                'sent': False,
                'scheduled_for': reminder_24h.isoformat(),
                'type': 'confirmation'
            },
            '2h': {
                'sent': False,
                'scheduled_for': reminder_2h.isoformat(),
                'type': 'final_reminder'
            }
        },
        'confirmed_by_client': False
    }
    
    bookings.append(test_booking)
    
    with open('data/bookings.json', 'w', encoding='utf-8') as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)
    
    print(f"Reserva de prueba creada:")
    print(f"   ID: {test_booking['id']}")
    print(f"   Fecha: {booking_date} {booking_time}")
    print(f"   Recordatorio 24h: {reminder_24h.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Recordatorio 2h: {reminder_2h.strftime('%Y-%m-%d %H:%M')}")

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

def main():
    print("SISTEMA DE PRUEBA DE RECORDATORIOS")
    print("==================================")
    
    while True:
        print("\nOpciones:")
        print("1. Crear reserva para manana")
        print("2. Crear reserva con recordatorio inmediato")
        print("3. Ejecutar verificacion de recordatorios")
        print("4. Salir")
        
        choice = input("\nElige una opcion (1-4): ").strip()
        
        if choice == '1':
            create_test_booking()
        elif choice == '2':
            test_immediate()
        elif choice == '3':
            reminder_service = ReminderService()
            reminder_service.check_and_send_reminders()
        elif choice == '4':
            break
        else:
            print("Opcion invalida")

if __name__ == "__main__":
    main()