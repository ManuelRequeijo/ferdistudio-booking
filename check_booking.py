import json
import os

def check_last_booking():
    print("=== VERIFICANDO ULTIMA RESERVA ===")
    
    bookings_file = 'data/bookings.json'
    
    if os.path.exists(bookings_file):
        with open(bookings_file, 'r', encoding='utf-8') as f:
            bookings = json.load(f)
        
        if bookings:
            last_booking = bookings[-1]
            print(f"Ultima reserva ID: {last_booking['id']}")
            print(f"Cliente: {last_booking['customer']['nombre']} {last_booking['customer']['apellido']}")
            print(f"Email cliente: {last_booking['customer']['email']}")
            print(f"Telefono cliente: {last_booking['customer']['telefono']}")
            print(f"Servicio: {last_booking['service_name']}")
            print(f"Fecha: {last_booking['date']}")
            print(f"Hora: {last_booking['time']}")
            
            # Verificar configuración
            from dotenv import load_dotenv
            load_dotenv()
            
            business_phone = os.getenv('BUSINESS_PHONE')
            print(f"\nTelefono del negocio (tu numero): {business_phone}")
            print(f"Telefono del cliente: {last_booking['customer']['telefono']}")
            
            if last_booking['customer']['telefono'] != business_phone:
                print("\n⚠️  PROBLEMA DETECTADO:")
                print("CallMeBot solo puede enviar mensajes DESDE tu numero autorizado")
                print("Pero estas intentando enviar AL numero del cliente")
                print("Necesitas cambiar la logica para enviar a TU numero")
            else:
                print("\n✅ Los numeros coinciden")
                
        else:
            print("No hay reservas")
    else:
        print("Archivo de reservas no existe")

if __name__ == "__main__":
    check_last_booking()