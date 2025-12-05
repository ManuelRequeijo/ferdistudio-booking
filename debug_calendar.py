#!/usr/bin/env python3
"""
Script para diagnosticar la integración con Google Calendar
"""
from datetime import datetime, date
from google_calendar import GoogleCalendarService

def debug_calendar():
    print("=== DEBUG GOOGLE CALENDAR ===")
    
    try:
        # Crear servicio
        calendar_service = GoogleCalendarService()
        
        if not calendar_service.service:
            print("ERROR: No se pudo conectar a Google Calendar")
            return
        
        print("Conexion exitosa con Google Calendar")
        
        # Obtener eventos de hoy
        today = date.today()
        print(f"Consultando eventos para: {today}")
        
        busy_times = calendar_service.get_busy_times(today)
        
        print(f"\nEventos encontrados: {len(busy_times)}")
        for i, event in enumerate(busy_times, 1):
            print(f"  {i}. {event['start']} - {event['end']}: {event['title']}")
        
        # Probar horario específico
        test_time = "18:00"
        duration = 60
        
        print(f"\nProbando disponibilidad:")
        print(f"Fecha: {today}")
        print(f"Hora: {test_time}")
        print(f"Duracion: {duration} minutos")
        
        is_available = calendar_service.is_time_available(today, test_time, duration)
        print(f"¿Está disponible? {is_available}")
        
        if not is_available:
            print("✓ CORRECTO: El horario está bloqueado")
        else:
            print("✗ PROBLEMA: El horario debería estar bloqueado")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_calendar()