#!/usr/bin/env python3
"""
Scheduler para recordatorios automáticos
Ejecuta cada hora para verificar y enviar recordatorios pendientes
"""
import schedule
import time
from datetime import datetime
from reminder_service import ReminderService

def run_reminder_check():
    """Ejecuta la verificación de recordatorios"""
    try:
        reminder_service = ReminderService()
        reminder_service.check_and_send_reminders()
    except Exception as e:
        print(f"Error en verificacion de recordatorios: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("Iniciando sistema de recordatorios automaticos...")
    print("Verificara recordatorios cada hora")
    print("Presiona Ctrl+C para detener")
    
    # Programar ejecución cada hora
    schedule.every().hour.do(run_reminder_check)
    
    # Ejecutar una vez al inicio para probar
    print("\nEjecutando verificacion inicial...")
    run_reminder_check()
    
    # Loop principal
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto si hay tareas pendientes
    except KeyboardInterrupt:
        print("\nSistema de recordatorios detenido")

if __name__ == "__main__":
    main()