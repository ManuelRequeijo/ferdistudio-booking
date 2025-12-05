#!/usr/bin/env python3
"""
Script para migrar reservas existentes al nuevo formato con recordatorios
"""
import json
import os
from datetime import datetime, timedelta

def migrate_bookings():
    """Migra reservas existentes para incluir sistema de recordatorios"""
    
    bookings_file = 'data/bookings.json'
    
    if not os.path.exists(bookings_file):
        print("❌ No se encontró archivo de reservas")
        return
    
    # Cargar reservas existentes
    with open(bookings_file, 'r', encoding='utf-8') as f:
        bookings = json.load(f)
    
    print(f"Migrando {len(bookings)} reservas...")
    
    updated_count = 0
    
    for booking in bookings:
        # Solo migrar si no tiene recordatorios
        if 'reminders' not in booking:
            try:
                # Calcular horarios de recordatorios
                booking_datetime = datetime.strptime(f"{booking['date']} {booking['time']}", '%Y-%m-%d %H:%M')
                reminder_24h = booking_datetime - timedelta(hours=24)
                reminder_2h = booking_datetime - timedelta(hours=2)
                
                # Agregar sistema de recordatorios
                booking['reminders'] = {
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
                }
                
                booking['confirmed_by_client'] = False
                
                # Si la reserva es del pasado, marcar recordatorios como enviados
                now = datetime.now()
                if booking_datetime <= now:
                    booking['reminders']['24h']['sent'] = True
                    booking['reminders']['2h']['sent'] = True
                    booking['reminders']['24h']['sent_at'] = 'migrated_past_booking'
                    booking['reminders']['2h']['sent_at'] = 'migrated_past_booking'
                
                updated_count += 1
                print(f"Migrada reserva #{booking['id']} - {booking['customer']['nombre']}")
                
            except Exception as e:
                print(f"Error migrando reserva #{booking['id']}: {e}")
    
    # Guardar reservas actualizadas
    if updated_count > 0:
        # Crear backup
        backup_file = f"{bookings_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(bookings, f, ensure_ascii=False, indent=2)
        print(f"Backup creado: {backup_file}")
        
        # Guardar versión migrada
        with open(bookings_file, 'w', encoding='utf-8') as f:
            json.dump(bookings, f, ensure_ascii=False, indent=2)
        
        print(f"Migracion completada: {updated_count} reservas actualizadas")
    else:
        print("No hay reservas para migrar")

def show_migration_preview():
    """Muestra qué reservas serían migradas"""
    
    bookings_file = 'data/bookings.json'
    
    if not os.path.exists(bookings_file):
        print("❌ No se encontró archivo de reservas")
        return
    
    with open(bookings_file, 'r', encoding='utf-8') as f:
        bookings = json.load(f)
    
    print(f"📋 PREVIEW DE MIGRACIÓN")
    print("=" * 50)
    
    to_migrate = []
    already_migrated = []
    
    for booking in bookings:
        if 'reminders' not in booking:
            to_migrate.append(booking)
        else:
            already_migrated.append(booking)
    
    print(f"✅ Ya migradas: {len(already_migrated)}")
    print(f"🔄 Por migrar: {len(to_migrate)}")
    
    if to_migrate:
        print(f"\nReservas que serán migradas:")
        for booking in to_migrate:
            print(f"  #{booking['id']} - {booking['customer']['nombre']} - {booking['date']} {booking['time']}")

def main():
    print("🔄 MIGRADOR DE RESERVAS")
    print("=" * 30)
    
    while True:
        print("\nOpciones:")
        print("1. Ver preview de migración")
        print("2. Ejecutar migración")
        print("3. Salir")
        
        choice = input("\nElige una opción (1-3): ").strip()
        
        if choice == '1':
            show_migration_preview()
        elif choice == '2':
            confirm = input("¿Estás seguro de migrar las reservas? (si/no): ").strip().lower()
            if confirm in ['si', 's', 'yes', 'y']:
                migrate_bookings()
            else:
                print("❌ Migración cancelada")
        elif choice == '3':
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    migrate_bookings()