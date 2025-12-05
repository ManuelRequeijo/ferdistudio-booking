#!/usr/bin/env python3
"""
Script para listar todos los calendarios disponibles
"""
from google_calendar import GoogleCalendarService

def list_calendars():
    print("=== LISTANDO CALENDARIOS ===")
    
    try:
        calendar_service = GoogleCalendarService()
        
        if not calendar_service.service:
            print("ERROR: No se pudo conectar a Google Calendar")
            return
        
        # Listar todos los calendarios
        calendars_result = calendar_service.service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])
        
        print(f"Calendarios encontrados: {len(calendars)}")
        print()
        
        for i, calendar in enumerate(calendars, 1):
            print(f"{i}. {calendar['summary']}")
            print(f"   ID: {calendar['id']}")
            print(f"   Primary: {calendar.get('primary', False)}")
            print(f"   Access Role: {calendar.get('accessRole', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    list_calendars()