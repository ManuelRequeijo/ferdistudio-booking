# 📧📱 Configuración de Notificaciones

## 🔧 Configuración de Email (Gmail)

### 1. Habilitar autenticación de 2 factores en Gmail
- Ve a tu cuenta de Google
- Seguridad → Verificación en 2 pasos → Activar

### 2. Generar contraseña de aplicación
- Google Account → Seguridad → Contraseñas de aplicaciones
- Selecciona "Correo" y "Otro"
- Copia la contraseña generada (16 caracteres)

### 3. Configurar en .env
```
EMAIL_USER=tu_email@gmail.com
EMAIL_PASSWORD=contraseña_de_aplicacion_de_16_caracteres
```

## 📱 Configuración de WhatsApp (CallMeBot - GRATIS)

### 1. Obtener API Key
- Envía un WhatsApp a: **+34 644 59 71 67**
- Mensaje: **"I allow callmebot to send me messages"**
- Te responderán con tu API Key

### 2. Configurar en .env
```
WHATSAPP_API_KEY=8953176
```

## ⚙️ Archivo .env Completo

Edita el archivo `.env` con tus datos:

```env
# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=tu_email@gmail.com
EMAIL_PASSWORD=tu_contraseña_de_aplicacion
EMAIL_FROM=Ferdistudio <tu_email@gmail.com>

# WhatsApp
WHATSAPP_API_KEY=tu_api_key_aqui

# Negocio
BUSINESS_NAME=Ferdistudio
BUSINESS_PHONE=+541136095284
BUSINESS_ADDRESS=Avenida Carabobo 276 A, Buenos Aires
```

## 🚀 Ejecutar

```bash
pip install -r requirements.txt
python run.py
```

## ✅ Prueba

1. Haz una reserva con tu email y teléfono
2. Deberías recibir:
   - ✉️ Email de confirmación
   - 📱 WhatsApp de confirmación

## 🔍 Solución de Problemas

**Email no llega:**
- Verifica que la contraseña de aplicación sea correcta
- Revisa la carpeta de spam

**WhatsApp no llega:**
- Verifica que enviaste el mensaje de autorización
- Usa el número con código de país (+54...)

**Errores en consola:**
- Revisa que el archivo .env tenga los datos correctos
- Verifica que las dependencias estén instaladas