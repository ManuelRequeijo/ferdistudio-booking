from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'ferdistudio-secret-2024'

class BookingSystem:
    def __init__(self):
        self.bookings_file = 'data/bookings.json'
        self.services = {
            'arreglo_barba': {'name': 'Arreglo de Barba', 'duration': 20, 'price': 15000},
            'corte': {'name': 'Corte', 'duration': 30, 'price': 20000},
            'corte_barba': {'name': 'Corte y Barba', 'duration': 60, 'price': 25000}
        }
        self.schedule = {
            'lunes': {'start': '11:00', 'end': '20:20'},
            'martes': {'start': '11:00', 'end': '20:20'},
            'miercoles': {'start': '11:00', 'end': '20:20'},
            'jueves': {'start': '12:20', 'end': '20:20'},
            'viernes': {'start': '11:00', 'end': '20:20'},
            'sabado': {'start': '10:00', 'end': '17:20'},
            'domingo': 'cerrado'
        }
        self.load_bookings()
    
    def load_bookings(self):
        if os.path.exists(self.bookings_file):
            with open(self.bookings_file, 'r', encoding='utf-8') as f:
                self.bookings = json.load(f)
        else:
            self.bookings = []
    
    def save_bookings(self):
        os.makedirs('data', exist_ok=True)
        with open(self.bookings_file, 'w', encoding='utf-8') as f:
            json.dump(self.bookings, f, ensure_ascii=False, indent=2)
    
    def get_available_slots(self, date, service_id):
        service = self.services[service_id]
        duration = service['duration']
        
        # Obtener día de la semana
        weekday = date.strftime('%A').lower()
        weekday_es = {
            'monday': 'lunes', 'tuesday': 'martes', 'wednesday': 'miercoles',
            'thursday': 'jueves', 'friday': 'viernes', 'saturday': 'sabado', 'sunday': 'domingo'
        }
        day_schedule = self.schedule.get(weekday_es[weekday])
        
        if day_schedule == 'cerrado':
            return []
        
        # Generar slots disponibles
        start_time = datetime.strptime(day_schedule['start'], '%H:%M').time()
        end_time = datetime.strptime(day_schedule['end'], '%H:%M').time()
        
        slots = []
        current = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
        
        # Inicializar Google Calendar con reintentos
        google_calendar = None
        google_calendar_working = False
        
        try:
            from google_calendar import GoogleCalendarService
            google_calendar = GoogleCalendarService()
            
            # Test rápido para verificar que funciona
            if google_calendar and google_calendar.service:
                test_events = google_calendar.get_busy_times(date)
                google_calendar_working = True
                print(f"Google Calendar activo - {len(test_events)} eventos encontrados")
            else:
                print("Google Calendar no disponible - usando solo reservas locales")
                
        except Exception as e:
            print(f"Error con Google Calendar: {e} - usando solo reservas locales")
            google_calendar = None
        
        while current + timedelta(minutes=duration) <= end_datetime:
            slot_time = current.strftime('%H:%M')
            
            # Verificar si el slot está ocupado en reservas locales
            is_available = True
            for booking in self.bookings:
                booking_date = datetime.strptime(booking['date'], '%Y-%m-%d').date()
                booking_time = booking['time']
                
                if booking_date == date and booking_time == slot_time:
                    is_available = False
                    break
            
            # Verificar disponibilidad en Google Calendar con reintentos
            if is_available and google_calendar and google_calendar_working:
                try:
                    is_available = google_calendar.is_time_available(date, slot_time, duration)
                except Exception as e:
                    print(f"Error consultando Google Calendar para {slot_time}: {e}")
                    # Si falla, mantener como disponible (solo usar reservas locales)
                    pass
            
            if is_available:
                slots.append(slot_time)
            
            current += timedelta(minutes=30)  # Intervalos de 30 minutos
        
        return slots
    
    def create_booking(self, service_id, date, time, customer_data):
        print(f"\nCREANDO RESERVA - Servicio: {service_id}, Cliente: {customer_data.get('nombre', 'Sin nombre')}")
        
        # Validar servicio
        if service_id not in self.services:
            raise ValueError(f"Servicio no válido: {service_id}")
        
        # Validar fecha y hora
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Formato de fecha inválido: {date}")
        
        if not time:
            raise ValueError("Hora requerida")
        
        # Sistema simplificado sin recordatorios automáticos
        
        booking = {
            'id': len(self.bookings) + 1,
            'service_id': service_id,
            'service_name': self.services[service_id]['name'],
            'price': self.services[service_id]['price'],
            'duration': self.services[service_id]['duration'],
            'date': date,
            'time': time,
            'customer': customer_data,
            'status': 'confirmed',
            'created_at': datetime.now().isoformat(),
            'contact_phone': '+541126510077'  # Solo para contacto manual
        }
        
        print(f"Guardando reserva #{booking['id']}")
        self.bookings.append(booking)
        self.save_bookings()
        
        # Crear evento en Google Calendar
        print(f"CREANDO EVENTO EN GOOGLE CALENDAR")
        try:
            from google_calendar import GoogleCalendarService
            google_calendar = GoogleCalendarService()
            if google_calendar and google_calendar.service:
                calendar_result = google_calendar.create_booking_event(booking)
                if calendar_result.get('success'):
                    booking['google_event_id'] = calendar_result['event_id']
                    booking['google_event_link'] = calendar_result['event_link']
                    print(f"Evento creado en Google Calendar: {calendar_result['event_id']}")
                else:
                    print(f"Error creando evento: {calendar_result.get('error', 'Unknown')}")
            else:
                print("Google Calendar no disponible")
        except Exception as e:
            print(f"Error con Google Calendar: {e}")
        
        # Enviar email de confirmación (en background para evitar timeout)
        print(f"ENVIANDO EMAIL DE CONFIRMACION")
        
        try:
            from notifications import NotificationService
            notification_service = NotificationService()
            # Timeout rápido para email
            result = notification_service.send_booking_confirmation(booking)
            print(f"Email enviado: {result.get('email_sent', False)}")
        except Exception as e:
            print(f"Error email: {str(e)[:100]}...")  # Truncar error largo
            # Continuar sin fallar
        
        return booking

booking_system = BookingSystem()

@app.route('/')
def index():
    return render_template('index.html', services=booking_system.services)

@app.route('/booking/<service_id>')
def booking_calendar(service_id):
    if service_id not in booking_system.services:
        return redirect(url_for('index'))
    
    service = booking_system.services[service_id]
    return render_template('calendar.html', service=service, service_id=service_id)

@app.route('/api/available-slots')
def get_available_slots():
    date_str = request.args.get('date')
    service_id = request.args.get('service_id')
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        slots = booking_system.get_available_slots(date, service_id)
        
        # Crear respuesta sin caché
        response = jsonify({'slots': slots, 'timestamp': datetime.now().isoformat()})
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/contact/<service_id>/<date>/<time>')
def contact_form(service_id, date, time):
    service = booking_system.services[service_id]
    return render_template('contact.html', 
                         service=service, 
                         service_id=service_id, 
                         date=date, 
                         time=time)

@app.route('/api/create-booking', methods=['POST'])
def create_booking():
    print("\n" + "="*50)
    print("API CREATE-BOOKING EJECUTANDOSE")
    print("="*50)
    
    try:
        data = request.get_json()
        print(f"DATOS RECIBIDOS: {data}")
        
        # Validar datos requeridos
        required_fields = ['service_id', 'date', 'time', 'customer']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo requerido faltante: {field}")
        
        # Validar datos del cliente
        customer = data['customer']
        customer_required = ['nombre', 'apellido', 'email', 'telefono']
        for field in customer_required:
            if field not in customer or not customer[field]:
                raise ValueError(f"Campo del cliente requerido: {field}")
        
        print(f"VALIDACION EXITOSA - Creando reserva...")
        
        # Crear reserva con timeout protection
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Timeout creando reserva")
        
        # Solo usar timeout en sistemas que lo soporten
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(30)  # 30 segundos timeout
        except:
            pass  # Windows no soporta SIGALRM
        
        try:
            booking = booking_system.create_booking(
                data['service_id'],
                data['date'],
                data['time'],
                data['customer']
            )
        finally:
            try:
                signal.alarm(0)  # Cancelar timeout
            except:
                pass
        
        print(f"RESERVA CREADA CON ID: {booking['id']}")
        print("="*50)
        
        return jsonify({
            'success': True,
            'booking_id': booking['id'],
            'message': 'Reserva creada exitosamente'
        })
        
    except TimeoutError as te:
        print(f"TIMEOUT ERROR: {te}")
        return jsonify({'success': False, 'error': 'Timeout procesando reserva'}), 408
    except ValueError as ve:
        print(f"ERROR DE VALIDACION: {ve}")
        return jsonify({'success': False, 'error': str(ve)}), 400
    except Exception as e:
        print(f"ERROR GENERAL: {e}")
        print(f"TIPO DE ERROR: {type(e).__name__}")
        return jsonify({'success': False, 'error': f'Error interno: {type(e).__name__}'}), 500

@app.route('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    booking = next((b for b in booking_system.bookings if b['id'] == booking_id), None)
    if not booking:
        return redirect(url_for('index'))
    
    return render_template('confirmation.html', booking=booking)

@app.route('/admin')
def admin_panel():
    from datetime import date, timedelta
    
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    # Contar reservas
    today_count = len([b for b in booking_system.bookings if b['date'] == today.strftime('%Y-%m-%d')])
    week_count = len([b for b in booking_system.bookings 
                     if week_start.strftime('%Y-%m-%d') <= b['date'] <= week_end.strftime('%Y-%m-%d')])
    total_revenue = sum(b['price'] for b in booking_system.bookings)
    
    # Ordenar reservas por fecha y hora (más recientes primero)
    sorted_bookings = sorted(booking_system.bookings, 
                           key=lambda x: (x['date'], x['time']), reverse=True)
    
    return render_template('admin.html', 
                         bookings=sorted_bookings,
                         today_count=today_count,
                         week_count=week_count,
                         total_revenue=total_revenue)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)