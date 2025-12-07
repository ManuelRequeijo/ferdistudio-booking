"""
Script para generar token.json para Google Calendar en producción
Ejecutar en local y luego subir el token.json generado
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']

def generate_token():
    # Usar credenciales del archivo local
    if os.path.exists('credentials.json'):
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=8081, open_browser=True)
        
        # Guardar token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
        print("✅ Token generado exitosamente!")
        print("📁 Archivo token.json creado")
        print("🚀 Ahora puedes usar Google Calendar en producción")
        
        return True
    else:
        print("❌ Archivo credentials.json no encontrado")
        return False

if __name__ == "__main__":
    generate_token()