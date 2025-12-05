import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_whatsapp():
    print("=== PRUEBA DE WHATSAPP ===")
    
    # Configuración
    api_key = os.getenv('WHATSAPP_API_KEY')
    phone = os.getenv('BUSINESS_PHONE')
    
    print(f"API Key: {api_key}")
    print(f"Teléfono: {phone}")
    
    # Limpiar número
    phone_clean = phone.replace('+', '').replace(' ', '').replace('-', '')
    print(f"Teléfono limpio: {phone_clean}")
    
    # Mensaje de prueba
    message = "Prueba de WhatsApp desde Ferdistudio - Sistema funcionando correctamente!"
    
    # URL de CallMeBot
    api_url = "https://api.callmebot.com/whatsapp.php"
    
    params = {
        'phone': phone_clean,
        'text': message,
        'apikey': api_key
    }
    
    print(f"\nURL: {api_url}")
    print(f"Parámetros: {params}")
    
    try:
        print("\nEnviando mensaje...")
        response = requests.get(api_url, params=params)
        
        print(f"Status Code: {response.status_code}")
        print(f"Respuesta: {response.text}")
        
        if response.status_code == 200:
            print("WHATSAPP ENVIADO EXITOSAMENTE")
            return True
        else:
            print(f"ERROR: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_whatsapp()