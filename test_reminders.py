#!/usr/bin/env python3
"""
Script para probar el sistema de recordatorios
"""
import json
from datetime import datetime, timedelta
from reminder_service import ReminderService

def create_test_booking():
    """Crea una reserva de prueba para mañana"""
    
    # Cargar reservas existentes
    try:
        with open('data/bookings.json', 'r', encoding='utf-8') as f:
            bookings = json.load(f)
    except:
        bookings = []
    
    # Crear reserva para mañana a las 14:00
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
            'telefono': '+541126510077',  # Tu número para pruebas
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
    
    # Guardar
    with open('data/bookings.json', 'w', encoding='utf-8') as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Reserva de prueba creada:")
    print(f"   ID: {test_booking['id']}")
    print(f"   Fecha: {booking_date} {booking_time}")
    print(f"   Recordatorio 24h: {reminder_24h.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Recordatorio 2h: {reminder_2h.strftime('%Y-%m-%d %H:%M')}")

def test_immediate_reminder():
    """Crea una reserva con recordatorio inmediato para probar"""
    
    try:
        with open('data/bookings.json', 'r', encoding='utf-8') as f:
            bookings = json.load(f)
    except:
        bookings = []
    
    # Crear reserva para dentro de 3 horas
    future_time = datetime.now() + timedelta(hours=3)
    booking_date = future_time.strftime('%Y-%m-%d')
    booking_time = future_time.strftime('%H:%M')
    
    # Recordatorio inmediato (ahora)
    reminder_now = datetime.now()
    
def test_last_minute_booking():
    """Crea una reserva de último minuto (menos de 24h)"""
    
    try:
        with open('data/bookings.json', 'r', encoding='utf-8') as f:
            bookings = json.load(f)
    except:
        bookings = []
    
    # Crear reserva para dentro de 2 horas (menos de 24h)
    future_time = datetime.now() + timedelta(hours=2)
    booking_date = future_time.strftime('%Y-%m-%d')
    booking_time = future_time.strftime('%H:%M')
    
    # Recordatorio inmediato
    reminder_now = datetime.now() + timedelta(minutes=1)
    
    test_booking = {
        'id': len(bookings) + 1,
        'service_id': 'corte',
        'service_name': 'Corte',
        'price': 20000,
        'duration': 30,
        'date': booking_date,
        'time': booking_time,
        'customer': {
            'nombre': 'Cliente',
            'apellido': 'UltimoMinuto',
            'email': 'test@example.com',
            'telefono': '+541126510077',
            'observaciones': 'Reserva de último minuto - menos de 24h'
        },
        'status': 'confirmed',
        'created_at': datetime.now().isoformat(),
        'reminders': {
            '24h': {
                'sent': False,
                'scheduled_for': reminder_now.isoformat(),  # Inmediato
                'type': 'confirmation'
            },
            '2h': {
                'sent': True,  # Saltado porque es muy tarde
                'scheduled_for': (future_time - timedelta(hours=2)).isoformat(),
                'type': 'final_reminder',
                'skipped_reason': 'too_late'
            }
        },
        'confirmed_by_client': False,
        'is_last_minute': True
    }
    
    bookings.append(test_booking)
    
    with open('data/bookings.json', 'w', encoding='utf-8') as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Reserva de último minuto creada:")
    print(f"   ID: {test_booking['id']}")
    print(f"   Fecha: {booking_date} {booking_time} (en 2 horas)")
    print(f"   Recordatorio: INMEDIATO")
    print(f"   Recordatorio 2h: SALTADO (muy tarde)")
    
    # Ejecutar recordatorios inmediatamente
    print(f"\n🚀 Ejecutando verificación de recordatorios...")
    reminder_service = ReminderService()
    reminder_service.check_and_send_reminders()
    
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
                'scheduled_for': reminder_now.isoformat(),  # Ahora mismo
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
    
    print(f"✅ Reserva de prueba inmediata creada:")
    print(f"   ID: {test_booking['id']}")
    print(f"   Recordatorio programado para: AHORA")
    
    # Ejecutar recordatorios inmediatamente
    print(f"\n🚀 Ejecutando verificación de recordatorios...")
    reminder_service = ReminderService()
    reminder_service.check_and_send_reminders()

def main():
    print("🧪 SISTEMA DE PRUEBA DE RECORDATORIOS")
    print("=====================================")
    
    while True:
        print("\nOpciones:")
        print("1. Crear reserva de prueba para mañana")
        print("2. Crear reserva con recordatorio inmediato")
        print("3. Crear reserva de último minuto (menos de 24h)")
        print("4. Ejecutar verificación de recordatorios")
        print("5. Ver reservas con recordatorios pendientes")
        print("6. Salir")
        
        choice = input("\nElige una opción (1-6): ").strip()
        
        if choice == '1':
            create_test_booking()
        elif choice == '2':
            test_immediate_reminder()
        elif choice == '3':
            test_last_minute_booking()
        elif choice == '4':
            reminder_service = ReminderService()
            reminder_service.check_and_send_reminders()
        elif choice == '5':
            show_pending_reminders()
        elif choice == '6':
            break
        else:
            print("❌ Opción inválida")

def show_pending_reminders():
    """Muestra reservas con recordatorios pendientes"""
    try:
        with open('data/bookings.json', 'r', encoding='utf-8') as f:
            bookings = json.load(f)
    except:
        print("❌ No se encontraron reservas")
        return
    
    print("\n📋 RESERVAS CON RECORDATORIOS PENDIENTES:")
    print("=" * 50)
    
    now = datetime.now()
    found = False
    
    for booking in bookings:
        # Solo mostrar reservas futuras
        booking_datetime = datetime.strptime(f"{booking['date']} {booking['time']}", '%Y-%m-%d %H:%M')
        if booking_datetime <= now:
            continue
        
        has_pending = False
        
        if not booking['reminders']['24h']['sent']:
            has_pending = True
        if not booking['reminders']['2h']['sent']:
            has_pending = True
        
        if has_pending:
            found = True
            print(f"\n🎯 Reserva #{booking['id']}")
            print(f"   Cliente: {booking['customer']['nombre']} {booking['customer']['apellido']}")
            print(f"   Fecha: {booking['date']} {booking['time']}")
            print(f"   Servicio: {booking['service_name']}")
            
            if not booking['reminders']['24h']['sent']:
                scheduled = datetime.fromisoformat(booking['reminders']['24h']['scheduled_for'])
                status = "⏰ LISTO" if now >= scheduled else f"⏳ {scheduled.strftime('%d/%m %H:%M')}"
                print(f"   Recordatorio 24h: {status}")
            else:
                print(f"   Recordatorio 24h: ✅ ENVIADO")
            
            if not booking['reminders']['2h']['sent']:
                scheduled = datetime.fromisoformat(booking['reminders']['2h']['scheduled_for'])
                status = "⏰ LISTO" if now >= scheduled else f"⏳ {scheduled.strftime('%d/%m %H:%M')}"
                print(f"   Recordatorio 2h: {status}")
            else:
                print(f"   Recordatorio 2h: ✅ ENVIADO")
    
    if not found:
        print("✅ No hay recordatorios pendientes")

if __name__ == "__main__":
    main()