# Proyecto Grúa Torre: Requerimientos Técnicos

## Contexto del Proyecto
Este proyecto implementa un sistema de control dual para una grúa torre a escala. El Arduino Nano lee joysticks locales y comandos remotos, mezcla ambas intenciones y controla dos motores DC y un motor paso a paso. El ESP32 sirve una interfaz web táctil y transmite los comandos al Arduino por UART.

## 1. Arquitectura de Hardware y Pines

### Arduino Nano (Actuador Principal)
- **Framework**: Arduino / C++
- **Responsabilidad**: Leer joysticks, interpretar comandos UART y manejar los drivers de potencia.
- **Asignación de Pines**:
  - **Joysticks**:
    - Carro (X) -> A0
    - Elevación (Y) -> A1
    - Giro (Z) -> A2
  - **Driver TB6612FNG (Motores DC)**:
    - Motor A (Carro): AIN1 = D2, AIN2 = D4, PWMA = D3
    - Motor B (Elevación): BIN1 = D7, BIN2 = D8, PWMB = D5
  - **Driver DRV8825 (Stepper para giro)**:
    - STEP = D9
    - DIR = D10
  - **Comunicación Serial**:
    - RX del Nano = conexión desde TX del ESP32

### ESP32 (Interfaz Web / Control de Red)
- **Framework**: MicroPython
- **Responsabilidad**: Servir la página web, recibir comandos del navegador y enviarlos por UART al Arduino.
- **Asignación de Pines**:
  - UART TX = GPIO 17 (hacia RX del Nano)
  - UART RX = GPIO 16 (si se usa enlace bidireccional)
  - LED de estado = GPIO 2

## 2. Funcionalidad de Software

### Firmware Arduino (`grua_arduino/grua_arduino.ino`)
- Lee los tres ejes del joystick analógico.
- Controla dos motores DC con PWM y un motor paso a paso con `AccelStepper`.
- Recibe comandos seriales de una sola letra desde el ESP32: `F`, `B`, `U`, `D`, `L`, `R`, `S`.
- Mantiene una intención web separada y suma la intención del joystick a la intención remota.
- Implementa un timeout de seguridad de 500 ms que reinicia las intenciones web si no llegan comandos nuevos.

### Firmware ESP32 (`esp32_server`)
- `boot.py`: menú de arranque interactivo, conectividad WiFi y modo REPL.
- `main.py`: servidor AP/híbrido con lectura de controles físicos de respaldo y manejo de comandos web.
- `telemetry.py`: servidor web asíncrono que expone `/`, `/api/command?cmd=` y `/api/telemetry`.
- `index.html`: interfaz de control remota con dos joysticks táctiles y botón de parada de emergencia.

## 3. Requisitos Clave
- **Comunicación UART**: 9600 bps, 8N1.
- **Comandos válidos**: `F`, `B`, `U`, `D`, `L`, `R`, `S`.
- **Seguridad**: Si no se recibe un comando web en 500 ms, el Arduino debe regresar a `S`.
- **Interfaz Web**: Control táctil, visualización minimalista y soporte para dispositivos móviles.

## 4. Resultados Esperados
- El Arduino debe poder mover el carro, subir/bajar el gancho y girar la pluma.
- El ESP32 debe servir la página remota y transmitir comandos válidos por UART.
- El sistema debe soportar control local por joystick y control remoto por navegador.

## 5. Archivos Principales
- `grua_arduino/grua_arduino.ino`
- `esp32_server/boot.py`
- `esp32_server/main.py`
- `esp32_server/telemetry.py`
- `esp32_server/index.html`
