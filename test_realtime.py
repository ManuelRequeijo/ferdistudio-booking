#!/usr/bin/env python3
"""
Test en tiempo real de Google Calendar
"""
from datetime import datetime, date
from google_calendar import GoogleCalendarService
import time

def test_realtime():
    print("=== TEST EN TIEMPO REAL ===")
    
    calendar_service = GoogleCalendarService()
    
    if not calendar_service.service:
        print("ERROR: No se pudo conectar")
        return
    
    today = date.today()
    
    print("Consultando eventos cada 5 segundos...")
    print("Crea/modifica/elimina eventos en tu celular y observa aqui")
    print("Presiona Ctrl+C para salir")
    
    try:
        while True:
            print(f"\n--- {datetime.now().strftime('%H:%M:%S')} ---")
            
            busy_times = calendar_service.get_busy_times(today)
            
            if busy_times:
                print(f"Eventos encontrados: {len(busy_times)}")
                for event in busy_times:
                    print(f"  {event['start']} - {event['end']}: {event['title']}")
            else:
                print("No hay eventos")
            
            # Test horario 18:00
            is_available = calendar_service.is_time_available(today, "18:00", 60)
            print(f"18:00 disponible: {is_available}")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nTest terminado")

if __name__ == "__main__":
    test_realtime()