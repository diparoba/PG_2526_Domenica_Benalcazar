## Why

Este cambio responde a la necesidad de simplificar la cinemática de giro reemplazando el motor a pasos por un motorreductor DC de 30 RPM, e implementar una separación de control explícita (Modo Web o Modo Manual con Joystick) activable de forma bidireccional desde la interfaz web o mediante el botón físico del joystick para mayor seguridad y flexibilidad.

## What Changes

- Reemplazo del motor a pasos por un motorreductor DC de 30 RPM en el mecanismo de giro, utilizando un puente H adicional (solo un canal).
- Adición de constantes de velocidad máxima configurables en el firmware del Arduino Nano para los tres motores (carro, elevación y giro).
- Implementación de un botón físico de joystick en el pin `D11` de Arduino Nano para alternar entre Modo de Control Web y Modo de Control Manual.
- Implementación de un switch toggle en la interfaz de usuario web (`index.html`) para alternar entre Modo de Control Web y Modo de Control Manual.
- **BREAKING**: El modo de control pasa a ser exclusivo (Web o Manual). Ya no se realiza la suma mixta analógica + remota; el sistema solo responde a la fuente de control activa.
- Creación de un esquema visual de conexiones electrónicas interactivo en `Schema.html`.

## Capabilities

### New Capabilities
- `electronic-schematic`: Documentación interactiva de todas las conexiones electrónicas en un archivo autónomo `Schema.html`.

### Modified Capabilities
- `communication_protocol`: Modificación de comandos UART para admitir el intercambio de estados del modo de control (`W` y `M`) y comandos de velocidad del motor de giro.
- `arduino_control_logic`: Modificación del control de giro de AccelStepper a driver DC de puente H, adición del procesamiento del botón de modo (`D11`) y exclusión de entradas según el modo de control.
- `esp32_web_api`: Adición de API para el switch de control web, monitorización bidireccional serial del modo de control y actualización del archivo `index.html`.
- `safety_system`: Ajuste del mecanismo del temporizador de seguridad (watchdog) para que solo aplique cuando el modo de control Web esté activo.

## Impact

- **Arduino (`grua_arduino.ino`)**: Remoción de librería AccelStepper, actualización de la máquina de estados de modo de control, antirrebote del botón de joystick, y cambio en los pines de potencia.
- **ESP32 (`main.py` y `telemetry.py`)**: Lectura de UART reactiva para sincronización del modo, nuevos endpoints HTTP `/api/status` y `/api/mode`.
- **Frontend (`index.html`)**: Incorporación de switch CSS para control de modo y rutina de polling periódico.
