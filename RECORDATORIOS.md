# 🔔 Sistema de Recordatorios Automáticos

## 📋 ¿Qué hace?

El sistema envía recordatorios automáticos por WhatsApp a los clientes:
- **24 horas antes**: Recordatorio con opción de confirmar/cancelar
- **2 horas antes**: Recordatorio final (solo si confirmó)

## 🚀 Cómo funciona

### 1. **Cuando se crea una reserva:**
- Se calculan automáticamente los horarios de recordatorios
- **Caso especial**: Si la reserva es con menos de 24h, envía recordatorio inmediato
- **Caso especial**: Si la reserva es con menos de 2h, salta el recordatorio de 2h
- Se guardan en la base de datos como "pendientes"

### 2. **El scheduler ejecuta cada hora:**
- Verifica si hay recordatorios pendientes
- Envía los que corresponden según la hora
- Marca como "enviados" los completados
- Maneja casos de último minuto automáticamente

### 3. **Mensajes automáticos:**

**24h antes (normal):**
```
🕐 ¡Hola Juan! Te recordamos tu cita mañana:
📅 10/12/2025 a las 14:00
✂️ Corte - $20,000
📍 Av. Carabobo 276A

¿Confirmas tu asistencia?
Responde:
✅ SI para confirmar
❌ NO para cancelar
```

**Reserva de último minuto:**
```
🚨 ¡Hola Juan! Confirmamos tu reserva:
📅 10/12/2025 a las 14:00
✂️ Corte - $20,000
📍 Av. Carabobo 276A

⚡ Reserva de último minuto confirmada
¡Te esperamos! 💈
```

**2h antes:**
```
⏰ ¡Tu cita es en 2 horas!
🕐 Hoy 14:00 - Corte
📍 Av. Carabobo 276A
¡Te esperamos! 💈
```

## 🛠️ Instalación

### 1. Instalar dependencias:
```bash
pip install schedule
```

### 2. Ejecutar el scheduler:
```bash
python reminder_scheduler.py
```

### 3. Para ejecutar en background:
```bash
# Windows
start /B python reminder_scheduler.py

# Linux/Mac
nohup python reminder_scheduler.py &
```

## 🧪 Pruebas

### Probar el sistema:
```bash
python test_reminders.py
```

Opciones disponibles:
1. **Crear reserva para mañana** - Prueba el flujo completo
2. **Recordatorio inmediato** - Prueba instantánea
3. **Reserva de último minuto** - Prueba con menos de 24h
4. **Ejecutar verificación** - Forzar envío de pendientes
5. **Ver pendientes** - Estado de recordatorios

### Verificar manualmente:
```bash
python reminder_service.py
```

## 📊 Beneficios

### Para Ferdi:
✅ Menos cancelaciones de último momento  
✅ Clientes más puntuales  
✅ Mejor planificación del día  
✅ Reducción de no-shows  

### Para Clientes:
✅ No se olvidan de la cita  
✅ Pueden cancelar con tiempo  
✅ Mejor experiencia de servicio  
✅ Recordatorios personalizados  

## 🔧 Configuración

### Variables de entorno necesarias:
```env
WHATSAPP_API_KEY=tu_api_key_callmebot
```

### Personalizar mensajes:
Edita las funciones en `reminder_service.py`:
- `send_24h_reminder()` - Mensaje de confirmación
- `send_2h_reminder()` - Recordatorio final

### Cambiar horarios:
En `app.py`, función `create_booking()`:
```python
reminder_24h = booking_datetime - timedelta(hours=24)  # 24h antes
reminder_2h = booking_datetime - timedelta(hours=2)    # 2h antes
```

## 📱 Respuestas de Clientes

Los clientes pueden responder:
- **"SI"** o **"✅"** → Confirma la cita
- **"NO"** o **"❌"** → Cancela la cita

*Nota: La funcionalidad de procesamiento de respuestas se puede implementar en una futura versión.*

## 🚨 Solución de Problemas

### El scheduler no envía mensajes:
1. Verificar que `WHATSAPP_API_KEY` esté configurado
2. Comprobar que hay reservas con recordatorios pendientes
3. Revisar logs en la consola

### Mensajes no llegan:
1. Verificar API key de CallMeBot
2. Comprobar formato del número de teléfono
3. Verificar conexión a internet

### Ver estado de recordatorios:
```bash
python test_reminders.py
# Opción 4: Ver reservas con recordatorios pendientes
```

## 🔄 Flujos del Sistema

**Flujo Normal:**
```
Cliente reserva → Sistema calcula recordatorios → Scheduler ejecuta cada hora → 
Envía 24h antes → Cliente confirma → Envía 2h antes → Cliente asiste
```

**Flujo Último Minuto (menos de 24h):**
```
Cliente reserva → Envía confirmación inmediata → 
Salta recordatorio 2h si es muy tarde → Cliente asiste
```

**Casos especiales:**
- ✅ Reserva con 12h de anticipación: Envía confirmación inmediata + recordatorio 2h antes
- ✅ Reserva con 1h de anticipación: Solo envía confirmación inmediata
- ✅ Reserva con 30min de anticipación: Solo envía confirmación inmediata

## 📈 Próximas Mejoras

- [ ] Procesamiento automático de respuestas de clientes
- [ ] Recordatorios por email además de WhatsApp
- [ ] Estadísticas de confirmaciones
- [ ] Recordatorios personalizables por servicio
- [ ] Integración con Google Calendar para recordatorios
