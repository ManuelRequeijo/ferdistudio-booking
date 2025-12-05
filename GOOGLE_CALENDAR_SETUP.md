# 📅 Configuración de Google Calendar

## 🔧 Pasos para integrar Google Calendar:

### 1. **Crear proyecto en Google Cloud Console**
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la **Google Calendar API**

### 2. **Crear credenciales**
1. Ve a "Credenciales" → "Crear credenciales" → "ID de cliente OAuth 2.0"
2. Tipo de aplicación: **Aplicación de escritorio**
3. Descarga el archivo JSON y renómbralo a `credentials.json`
4. Colócalo en la carpeta raíz del proyecto

### 3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 4. **Primera autenticación**
1. Ejecuta la aplicación: `python app.py`
2. La primera vez te pedirá autorización en el navegador
3. Se creará automáticamente el archivo `token.json`

### 5. **Configurar calendario (opcional)**
- Por defecto usa tu calendario principal
- Para usar otro calendario, actualiza `GOOGLE_CALENDAR_ID` en `.env`

## ✅ **Cómo funciona:**

1. **Sincronización automática**: Cada vez que alguien consulta horarios, se verifica Google Calendar
2. **Bloqueo inteligente**: Si tienes una cita personal, ese horario no aparece disponible
3. **Tiempo real**: Los cambios en Google Calendar se reflejan inmediatamente

## 🎯 **Beneficios:**

- **Gestión centralizada**: Todo desde Google Calendar
- **Sincronización automática**: Sin intervención manual
- **Flexibilidad**: Bloquea horarios para citas personales
- **Confiabilidad**: Evita dobles reservas

## 🔄 **Uso diario:**

1. **Bloquear horarios**: Crea eventos en Google Calendar
2. **Citas personales**: Se bloquean automáticamente
3. **Vacaciones**: Bloquea días completos
4. **Cambios de horario**: Actualiza y se sincroniza al instante

## ⚠️ **Nota:**
Si no configuras Google Calendar, el sistema funciona normalmente con los horarios fijos del código.