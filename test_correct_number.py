import requests

def test_correct_number():
    print("=== PROBANDO CON NUMERO CORRECTO ===")
    
    # Usar el número exacto que CallMeBot tiene registrado
    phone_callmebot = "549112651007"  # Del mensaje de CallMeBot
    api_key = "5052492"
    message = "Prueba con numero correcto"
    
    # Construir URL
    api_url = f"https://api.callmebot.com/whatsapp.php?phone={phone_callmebot}&text={message}&apikey={api_key}"
    
    print(f"Número en CallMeBot: {phone_callmebot}")
    print(f"Número en .env: 541126510077")
    print(f"URL: {api_url}")
    
    try:
        response = requests.get(api_url)
        print(f"\nStatus: {response.status_code}")
        print(f"Respuesta: {response.text}")
        
        if 'invalid' not in response.text.lower():
            print("\n✅ FUNCIONA CON EL NUMERO CORRECTO!")
        else:
            print("\n❌ Sigue fallando")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_correct_number()