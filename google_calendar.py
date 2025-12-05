import os
from datetime import datetime, timedelta
import pytz
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class GoogleCalendarService:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.calendar_id = os.getenv('GOOGLE_CALENDAR_ID', 'primary')
        self.service = None
        self.cache = {}  # Cache para eventos
        self.cache_expiry = 60  # Cache expira en 60 segundos
        self.authenticate()
    
    def authenticate(self):
        """Autenticar con Google Calendar API"""
        creds = None
        
        try:
            # Token guardado de sesiones anteriores
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
            
            # Si no hay credenciales válidas, obtener nuevas
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except Exception as e:
                        print(f"Error refrescando token: {e}")
                        # Eliminar token corrupto
                        if os.path.exists('token.json'):
                            os.remove('token.json')
                        creds = None
                
                if not creds:
                    if os.path.exists('credentials.json'):
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials.json', self.SCOPES)
                        # Usar puerto específico para evitar conflictos
                        creds = flow.run_local_server(port=8080, open_browser=True)
                    else:
                        print("Error: Archivo credentials.json no encontrado")
                        return False
                
                # Guardar credenciales para próximas ejecuciones
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            
            self.service = build('calendar', 'v3', credentials=creds)
            print("Autenticacion con Google Calendar exitosa")
            return True
            
        except Exception as e:
            print(f"Error en autenticacion: {e}")
            return False
    
    def get_busy_times(self, date):
        """Obtener horarios ocupados de Google Calendar para una fecha específica"""
        if not self.service:
            return []
        
        # Verificar cache
        cache_key = f"{date}_{self.calendar_id}"
        now = datetime.now().timestamp()
        
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if now - timestamp < self.cache_expiry:
                return cached_data
        
        try:
            # Zona horaria de Argentina
            tz = pytz.timezone('America/Argentina/Buenos_Aires')
            
            # Definir rango del día en zona horaria local
            start_time = tz.localize(datetime.combine(date, datetime.min.time()))
            end_time = start_time + timedelta(days=1)
            
            # Consultar eventos del día
            
            # Consultar eventos del día
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=start_time.isoformat(),
                timeMax=end_time.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            busy_times = []
            
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                # Solo procesar eventos con hora específica
                if start and end and 'T' in str(start) and 'T' in str(end):
                    try:
                        # Parsear fechas con zona horaria
                        if start.endswith('Z'):
                            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                        else:
                            start_dt = datetime.fromisoformat(start)
                        
                        if end.endswith('Z'):
                            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                        else:
                            end_dt = datetime.fromisoformat(end)
                        
                        # Convertir a zona horaria local
                        tz = pytz.timezone('America/Argentina/Buenos_Aires')
                        if start_dt.tzinfo is None:
                            start_dt = tz.localize(start_dt)
                        else:
                            start_dt = start_dt.astimezone(tz)
                        
                        if end_dt.tzinfo is None:
                            end_dt = tz.localize(end_dt)
                        else:
                            end_dt = end_dt.astimezone(tz)
                        
                        busy_times.append({
                            'start': start_dt.strftime('%H:%M'),
                            'end': end_dt.strftime('%H:%M'),
                            'title': event.get('summary', 'Ocupado')
                        })
                        
                    except Exception as e:
                        pass  # Ignorar eventos con formato incorrecto
            
            # Guardar en cache
            self.cache[cache_key] = (busy_times, now)
            
            return busy_times
            
        except Exception as e:
            print(f"Error consultando Google Calendar: {e}")
            # Si hay error, devolver cache anterior si existe
            if cache_key in self.cache:
                cached_data, _ = self.cache[cache_key]
                return cached_data
            return []
    
    def is_time_available(self, date, time, duration_minutes):
        """Verificar si un horario específico está disponible"""
        busy_times = self.get_busy_times(date)
        
        # Convertir tiempo solicitado a datetime
        requested_start = datetime.combine(date, datetime.strptime(time, '%H:%M').time())
        requested_end = requested_start + timedelta(minutes=duration_minutes)
        
        for busy in busy_times:
            busy_start = datetime.combine(date, datetime.strptime(busy['start'], '%H:%M').time())
            busy_end = datetime.combine(date, datetime.strptime(busy['end'], '%H:%M').time())
            
            # Verificar si hay conflicto
            if (requested_start < busy_end and requested_end > busy_start):
                return False
        
        return True
    
    def create_booking_event(self, booking):
        """Crear evento en Google Calendar para una reserva"""
        if not self.service:
            return False
        
        try:
            # Zona horaria de Argentina
            tz = pytz.timezone('America/Argentina/Buenos_Aires')
            
            # Parsear fecha y hora de la reserva
            booking_date = datetime.strptime(booking['date'], '%Y-%m-%d').date()
            booking_time = datetime.strptime(booking['time'], '%H:%M').time()
            
            # Crear datetime con zona horaria
            start_datetime = tz.localize(datetime.combine(booking_date, booking_time))
            end_datetime = start_datetime + timedelta(minutes=booking.get('duration', 60))
            
            # Crear evento
            event = {
                'summary': f"Cliente: {booking['customer']['nombre']} - {booking['service_name']}",
                'description': f"Cliente: {booking['customer']['nombre']} {booking['customer']['apellido']}\n"
                              f"Telefono: {booking['customer']['telefono']}\n"
                              f"Email: {booking['customer']['email']}\n"
                              f"Servicio: {booking['service_name']}\n"
                              f"Precio: ${booking['price']:,}\n"
                              f"ID Reserva: #{booking['id']}",
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': 'America/Argentina/Buenos_Aires',
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': 'America/Argentina/Buenos_Aires',
                },
                'colorId': '2',
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            
            # Insertar evento
            created_event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()
            
            print(f"Evento creado en Google Calendar: {created_event['id']}")
            
            # Limpiar cache
            cache_key = f"{booking_date}_{self.calendar_id}"
            if cache_key in self.cache:
                del self.cache[cache_key]
            
            return {
                'success': True,
                'event_id': created_event['id'],
                'event_link': created_event.get('htmlLink', '')
            }
            
        except Exception as e:
            print(f"Error creando evento en Google Calendar: {e}")
            return {'success': False, 'error': str(e)}