#!/usr/bin/env python3
"""
Script para crear un evento de prueba y verificar que funciona
"""
from datetime import datetime, timedelta
import pytz
from google_calendar import GoogleCalendarService

def create_test_event():
    print("=== CREANDO EVENTO DE PRUEBA ===")
    
    try:
        calendar_service = GoogleCalendarService()
        
        if not calendar_service.service:
            print("ERROR: No se pudo conectar a Google Calendar")
            return
        
        # Zona horaria de Argentina
        tz = pytz.timezone('America/Argentina/Buenos_Aires')
        
        # Crear evento para dentro de 10 minutos
        now = datetime.now(tz)
        start_time = now + timedelta(minutes=10)
        end_time = start_time + timedelta(hours=1)
        
        event = {
            'summary': 'PRUEBA - Evento creado por sistema',
            'description': 'Este es un evento de prueba creado automaticamente',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/Argentina/Buenos_Aires',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/Argentina/Buenos_Aires',
            },
        }
        
        print(f"Creando evento de {start_time.strftime('%H:%M')} a {end_time.strftime('%H:%M')}")
        
        # Crear el evento
        event_result = calendar_service.service.events().insert(
            calendarId='primary', 
            body=event
        ).execute()
        
        print(f"Evento creado exitosamente!")
        print(f"ID del evento: {event_result['id']}")
        print(f"Link: {event_result.get('htmlLink', 'N/A')}")
        
        # Ahora verificar que lo podemos leer
        print("\n=== VERIFICANDO QUE SE PUEDE LEER ===")
        
        today = start_time.date()
        busy_times = calendar_service.get_busy_times(today)
        
        print(f"Eventos encontrados: {len(busy_times)}")
        for event in busy_times:
            print(f"  - {event['start']} - {event['end']}: {event['title']}")
        
        # Verificar disponibilidad
        test_time = start_time.strftime('%H:%M')
        is_available = calendar_service.is_time_available(today, test_time, 60)
        
        print(f"\nProbando disponibilidad para {test_time}:")
        print(f"¿Está disponible? {is_available}")
        
        if not is_available:
            print("EXITO: El sistema detecta correctamente el evento!")
        else:
            print("PROBLEMA: El sistema no detecta el evento")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_test_event()