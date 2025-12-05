#!/usr/bin/env python3
"""
Script de prueba para verificar la autenticación con Google Calendar
"""
import os
from google_calendar import GoogleCalendarService
from datetime import datetime, date

def test_google_calendar():
    print("Probando autenticacion con Google Calendar...")
    
    try:
        # Crear instancia del servicio
        calendar_service = GoogleCalendarService()
        
        if calendar_service.service:
            print("Autenticacion exitosa!")
            
            # Probar obtener eventos de hoy
            today = date.today()
            print(f"Consultando eventos para: {today}")
            
            busy_times = calendar_service.get_busy_times(today)
            
            if busy_times:
                print(f"Eventos encontrados ({len(busy_times)}):")
                for event in busy_times:
                    print(f"  - {event['start']} - {event['end']}: {event['title']}")
            else:
                print("No hay eventos para hoy")
            
            print("\nGoogle Calendar configurado correctamente!")
            return True
            
        else:
            print("Error en la autenticacion")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_google_calendar()