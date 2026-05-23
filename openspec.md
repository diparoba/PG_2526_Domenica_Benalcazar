# OpenSpec: Sistema de Control de Grúa Torre

## 1. Protocolo de Comunicación (UART)
- Baudrate: `9600` bps.
- Formato: `8N1`.
- Conexión principal: ESP32 TX (GPIO 17) hacia Arduino RX.
- Comandos soportados:
  - `F` = Avanzar carro
  - `B` = Retroceder carro
  - `U` = Subir gancho
  - `D` = Bajar gancho
  - `L` = Girar pluma a la izquierda
  - `R` = Girar pluma a la derecha
  - `S` = Stop / Parada de emergencia

## 2. Lógica de Control en Arduino
- El Arduino Nano lee:
  - Joystick X en `A0` (control del carro)
  - Joystick Y en `A1` (control de elevación)
  - Joystick Z en `A2` (control de giro)
- Controla motores DC mediante TB6612FNG:
  - Motor A (Carro): `AIN1=D2`, `AIN2=D4`, `PWMA=D3`
  - Motor B (Elevación): `BIN1=D7`, `BIN2=D8`, `PWMB=D5`
- Controla el motor paso a paso mediante DRV8825:
  - `STEP=D9`, `DIR=D10`
- La intención local de joystick se suma con la intención remota recibida por UART.
- Si no se recibe un comando web válido en `500 ms`, la intención remota se reinicia a cero.

## 3. API Web del ESP32
### Endpoints disponibles
- `GET /` - Devuelve la interfaz remota `index.html`.
- `GET /api/command?cmd={F|B|U|D|L|R|S}` - Envía un comando al Arduino.
- `GET /api/telemetry` - Devuelve registros de evento (solo si el servidor de telemetría está activo).

### Respuestas
- Comando válido: `200 OK`, `Content-Type: application/json`, `{"status":"ok"}`.
- Comando inválido: `400 Bad Request`.
- Recurso no encontrado: `404 Not Found`.

## 4. Comportamiento de la Interfaz Web
- El cliente usa `fetch()` para enviar comandos sin recarga.
- La página `index.html` implementa dos mandos táctiles:
  - Joystick circular para `F`, `B`, `L`, `R`.
  - Joystick lineal para `U` y `D`.
- Un botón de emergencia envía `S` inmediatamente.

## 5. Modos ESP32 actuales
- `esp32_server/boot.py` proporciona un menú de inicio y configuración WiFi.
- `esp32_server/main.py` actúa como servidor AP local y como lector de controles físicos.
- `esp32_server/telemetry.py` contiene el servidor web asíncrono que expone `/`, `/api/command` y `/api/telemetry`.

## 6. Reglas de seguridad
- `S` debe ser el estado de reposo si no hay movimientos activos.
- El Arduino debe detener los motores si el comando web deja de llegar o si la interfaz física de respaldo lo solicita.
