#!/usr/bin/env python3
"""
Script para eliminar eventos de prueba
"""
from datetime import datetime, date
from google_calendar import GoogleCalendarService

def delete_test_events():
    print("=== ELIMINANDO EVENTOS DE PRUEBA ===")
    
    try:
        calendar_service = GoogleCalendarService()
        
        if not calendar_service.service:
            print("ERROR: No se pudo conectar a Google Calendar")
            return
        
        # Obtener eventos de hoy
        today = date.today()
        busy_times = calendar_service.get_busy_times(today)
        
        print(f"Eventos encontrados: {len(busy_times)}")
        
        # Buscar eventos que contengan "PRUEBA"
        events_result = calendar_service.service.events().list(
            calendarId='primary',
            q='PRUEBA',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        for event in events:
            event_id = event['id']
            summary = event.get('summary', 'Sin titulo')
            
            print(f"Eliminando: {summary}")
            
            calendar_service.service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()
            
            print(f"Evento eliminado: {event_id}")
        
        print("Eventos de prueba eliminados")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    delete_test_events()