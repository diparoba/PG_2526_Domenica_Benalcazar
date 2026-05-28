## Why

El módulo inalámbrico (ESP32) sufre de inestabilidad y cuellos de botella al procesar peticiones web concurrentes pesadas. Se requiere migrar el control principal al cable USB directo usando Web Serial API en el navegador, y reorientar el ESP32 únicamente como monitor inalámbrico de logs.

## What Changes

- **BREAKING**: Reemplazo de la API HTTP de control en ESP32 por control local por cable USB usando la Web Serial API nativa de Chrome/Edge en `index.html`.
- **BREAKING**: Reorientación del ESP32 a un monitor de depuración inalámbrica. Lee logs seriales del Arduino y sirve una página HTML retro de terminal de logs.
- Adición de un puerto serial secundario emulado por software (SoftwareSerial en pines D12/D9) en Arduino Nano para enviar logs textuales al ESP32.
- Adición de enlaces cruzados en las cabeceras de `index.html` y `Schema.html` para navegación fluida.
- Reorganización total de los archivos del proyecto en carpetas específicas: `/arduino/`, `/esp32/` y `/web_server/`, eliminando duplicados obsoletos de la raíz.

## Capabilities

### New Capabilities
- `web-serial-control`: Control directo bidireccional y recepción de telemetría en la UI web mediante la Web Serial API nativa sobre USB.
- `wireless-debug-monitor`: Transmisión de logs desde Arduino vía SoftwareSerial y servidor web de depuración minimalista en ESP32 (puerto 80) para lectura remota.
- `project-file-structure`: Organización física del repositorio en directorios dedicados y eliminación de archivos redundantes en la raíz.

### Modified Capabilities
- `communication_protocol`: Ajuste para enviar telemetría en formato JSON por hardware serial (USB) y redirigir logs textuales a SoftwareSerial.
- `arduino_control_logic`: Modificación del procesamiento de comandos de entrada a través de hardware serial USB y envío de logs a SoftwareSerial.
- `esp32_web_api`: Eliminación de los endpoints de control (`/api/command`), y adición del servicio de logs del terminal HTML en el puerto 80.
- `electronic-schematic`: Actualización del esquema `Schema.html` para incluir la conexión de SoftwareSerial y la organización de carpetas.

## Impact

- **Arduino (`/arduino/grua_arduino.ino`)**: Implementación de SoftwareSerial, desactivación de watchdog serial de 500ms al operar localmente por USB, y salida de telemetría JSON.
- **ESP32 (`/esp32/main.py`)**: Remoción del bucle de control, adición de buffer de logs en anillo (RAM, 50 líneas) y servidor web simple.
- **Interfaz (`/web_server/index.html`)**: Incorporación de controles Web Serial, botón de conectar, decodificación JSON de telemetría, y navegación cruzada.
- **Esquema (`/web_server/Schema.html`)**: Actualización de conexiones físicas de SoftwareSerial y navegación cruzada.
