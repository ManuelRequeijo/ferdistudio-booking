import os
import requests
from dotenv import load_dotenv

load_dotenv()

def debug_whatsapp():
    print("=== DEBUG WHATSAPP ===")
    
    # Configuración
    api_key = os.getenv('WHATSAPP_API_KEY')
    phone = os.getenv('BUSINESS_PHONE')
    
    print(f"API Key desde .env: '{api_key}'")
    print(f"Teléfono desde .env: '{phone}'")
    
    # Limpiar número
    phone_clean = phone.replace('+', '').replace(' ', '').replace('-', '')
    print(f"Teléfono limpio: '{phone_clean}'")
    
    # Mensaje simple
    message = "Test"
    
    # Construir URL exacta
    base_url = "https://api.callmebot.com/whatsapp.php"
    full_url = f"{base_url}?phone={phone_clean}&text={message}&apikey={api_key}"
    
    print(f"\nURL completa que enviamos:")
    print(f"{full_url}")
    
    print(f"\nPor favor compara esta URL con el enlace que te dio CallMeBot")
    print(f"¿Son similares los parámetros?")
    
    # Hacer la petición
    try:
        print(f"\nHaciendo petición...")
        response = requests.get(full_url)
        print(f"Status: {response.status_code}")
        print(f"Respuesta completa:")
        print(f"{response.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_whatsapp()