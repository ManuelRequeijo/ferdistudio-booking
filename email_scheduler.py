import schedule
import time
from email_reminder_service import EmailReminderService

def run_email_reminders():
    """Ejecuta el servicio de recordatorios por email"""
    try:
        reminder_service = EmailReminderService()
        reminder_service.check_and_send_reminders()
    except Exception as e:
        print(f"Error en scheduler de email: {e}")

# Programar ejecución cada hora
schedule.every().hour.do(run_email_reminders)

print("Email Scheduler iniciado - verificando cada hora")
print("Presiona Ctrl+C para detener")

# Ejecutar una vez al inicio
run_email_reminders()

# Loop principal
while True:
    try:
        schedule.run_pending()
        time.sleep(60)  # Verificar cada minuto
    except KeyboardInterrupt:
        print("\nScheduler detenido")
        break
    except Exception as e:
        print(f"Error en scheduler: {e}")
        time.sleep(60)