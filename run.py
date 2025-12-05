import os
import sys

def main():
    os.makedirs('data', exist_ok=True)
    
    if sys.version_info < (3, 7):
        print("Se requiere Python 3.7+")
        return
    
    print("Iniciando Ferdistudio Booking System...")
    print("Disponible en: http://localhost:5001")
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5001)
    except ImportError:
        print("Error: Instala las dependencias con 'pip install -r requirements.txt'")
    except KeyboardInterrupt:
        print("\nServidor detenido")

if __name__ == "__main__":
    main()