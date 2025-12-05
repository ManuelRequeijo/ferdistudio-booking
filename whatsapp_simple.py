import urllib.parse

def crear_enlace_whatsapp(telefono, mensaje):
    """Crea un enlace de WhatsApp simple"""
    # Limpiar número
    telefono_limpio = telefono.replace('+', '').replace(' ', '').replace('-', '')
    
    # Codificar mensaje
    mensaje_codificado = urllib.parse.quote(mensaje)
    
    # Crear enlace
    enlace = f"https://wa.me/{telefono_limpio}?text={mensaje_codificado}"
    
    return enlace

def generar_mensaje_reserva(booking):
    """Genera el mensaje de WhatsApp para la reserva"""
    customer = booking['customer']
    
    mensaje = f"""🎉 *RESERVA CONFIRMADA - Ferdistudio*

Hola {customer['nombre']}! Tu cita está confirmada:

📋 *Detalles:*
• Servicio: {booking['service_name']}
• Fecha: {booking['date']}
• Hora: {booking['time']}
• Precio: ${booking['price']:,}

📍 *Ubicación:*
Avenida Carabobo 276 A, Buenos Aires

¡Gracias por elegir Ferdistudio! 💈"""
    
    return mensaje

def procesar_whatsapp(booking):
    """Procesa el WhatsApp para una reserva"""
    try:
        telefono = booking['customer']['telefono']
        mensaje = generar_mensaje_reserva(booking)
        enlace = crear_enlace_whatsapp(telefono, mensaje)
        
        print(f"\n📱 WhatsApp para: {telefono}")
        print(f"🔗 ENLACE: {enlace}")
        print(f"📝 Mensaje: {mensaje[:100]}...")
        print("\n✅ COPIA EL ENLACE Y ÁBRELO EN TU NAVEGADOR")
        
        return True
    except Exception as e:
        print(f"❌ Error WhatsApp: {e}")
        return False