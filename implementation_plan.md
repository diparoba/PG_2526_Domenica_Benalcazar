# Plan de Implementación de Grúa Torre (Arduino Nano + ESP32)

Este documento describe la implementación real del sistema de control dual para la grúa torre, usando los archivos presentes en el repositorio.

## Arquitectura General
- **Arduino Nano** ejecuta `grua_arduino/grua_arduino.ino`.
- **ESP32** ejecuta `esp32_server/boot.py` y `esp32_server/main.py` o `esp32_server/telemetry.py` según la versión.
- **Interfaz Web**: `esp32_server/index.html`.

## Requisitos del Proyecto
1. Control de dos motores DC con TB6612FNG y un motor paso a paso con DRV8825.
2. Control dual local-remoto: joysticks analógicos + navegador web.
3. Comunicación UART a 9600 bps entre ESP32 y Arduino.
4. Interfaz web táctil para enviar comandos remotos.
5. Seguridad: timeout de comando web y parada de emergencia.

## Estado Actual
- `grua_arduino/grua_arduino.ino` está implementado y controla el hardware mediante dos motores DC y un stepper.
- `esp32_server/main.py` implementa un servidor AP/híbrido de respaldo con lectura de botones físicos.
- `esp32_server/telemetry.py` implementa un servidor web asíncrono que expone `/`, `/api/command` y `/api/telemetry`.
- `esp32_server/index.html` ofrece una UI de control remoto con joysticks y un botón de emergencia.

## Diseño de Software

### Arduino Nano
- Joysticks analógicos en `A0`, `A1`, `A2`.
- Control de motores DC:
  - Motor A (Carro): `AIN1=D2`, `AIN2=D4`, `PWMA=D3`.
  - Motor B (Elevación): `BIN1=D7`, `BIN2=D8`, `PWMB=D5`.
- Control de stepper: `STEP=D9`, `DIR=D10`.
- Interpreta comandos UART `F,B,U,D,L,R,S`.
- Suma la intención del joystick local con la intención remota.
- Timeout de seguridad web de 500 ms para resetear la intención remota.

### ESP32
- `boot.py` proporciona menú de inicio y configuración WiFi.
- `main.py` funciona como servidor AP local y lee controles físicos de respaldo.
- `telemetry.py` funciona como servidor web `uasyncio` para la página remota.
- `index.html` envía comandos con `fetch('/api/command?cmd=...')`.

## Archivo Clave de Interfaz
- `esp32_server/index.html` usa un joystick circular para `F/B/L/R`, un joystick lineal para `U/D` y un botón de emergencia para `S`.

## Verificación
1. Revisar que las rutas y los endpoints web correspondan con `main.py`/`telemetry.py`.
2. Confirmar que Arduino reciba y aplique correctamente `F/B/U/D/L/R/S`.
3. Probar que la UI remota funcione en el navegador y que el botón E-Stop envíe `S`.
4. Verificar el timeout de 500 ms en el firmware Arduino.

## Consideraciones Técnicas
- Las funcionalidades de servidor web y de control físico se pueden ejecutar en dos scripts distintos (`main.py` y `telemetry.py`) según el modo de uso.
- El documento actual describe el estado real del repositorio, no una versión hipotética.
