# Plan de Implementación de Grúa Torre (Arduino Nano + ESP32)

Este documento detalla la arquitectura, el diseño y la implementación del sistema de control dual (manual y web) para una grúa torre, basado en los requerimientos técnicos proporcionados (v2).

## Requisitos del Proyecto
1. **Control de Motores**: 
   - Eje de rotación (Giro): Motor a pasos Nema 17 con driver DRV8825. (Movimiento suave con `AccelStepper`).
   - Eje Carro (Adelante/Atrás): Motor DC con driver TB6612FNG (Motor A).
   - Eje Elevación (Subir/Bajar): Motor DC con driver TB6612FNG (Motor B).
2. **Control Dual**: Joysticks (Manual) y Web (Remoto). Lógica mixta: se sumará la intención del joystick con la intención web.
3. **Microcontroladores**: Arduino Nano (Hardware/Motores) y ESP32 en MicroPython (Servidor Web).
4. **Documentación**: Estándar OpenSpec documentando la lógica de control, mensajería UART y endpoints web.
5. **Seguridad**: Timeout para comandos web (detención si no se recibe un comando continuo).

## Open Questions
- El diseño web pide "Diseño minimalista tipo Control Remoto", pero también instrucciones globales de usar diseño muy moderno (Glassmorphism, animaciones). Integraré un diseño de "Control Remoto" que sea premium, responsivo y estético.
- ¿Hay algún SSID y Password por defecto que desees en `boot.py` o los dejo genéricos (ej. `SSID="WIFI_GRUA"`, `PASS="12345678"`)? *Por defecto usaré datos genéricos que podrás modificar.*

## Proposed Changes

---

### Arquitectura de Pines y Hardware

#### Arduino Nano
- **Driver TB6612FNG (Motores DC N20):**
  - Motor A (Carro): `AIN1` (D2), `AIN2` (D4), `PWMA` (D3).
  - Motor B (Elevación): `BIN1` (D7), `BIN2` (D8), `PWMB` (D5).
  - `STBY`: VCC (5V).
- **Driver DRV8825 (Nema 17 - Giro):**
  - `STEP`: Pin D9
  - `DIR`: Pin D10
- **Joysticks:**
  - `X` (Carro): Pin A0
  - `Y` (Elevación): Pin A1
  - `Giro`: Pin A2
- **Comunicación ESP32 (Hardware Serial a 9600 bps):**
  - `RX`: Pin D0 (Conectado al TX del ESP32).

#### ESP32 DevKit V1
- **UART a Arduino Nano:**
  - `TX`: GPIO 17 (Conectado a RX del Nano).
- **Status LED:**
  - `LED`: GPIO 2.

---

### Archivos a Generar

#### [NEW] `grua_arduino/grua_arduino.ino`
- Integración de `TB6612FNG` y `AccelStepper`.
- Lectura de Joysticks (A0, A1, A2).
- Parser UART simple a 9600 baudios: 'F', 'B', 'U', 'D', 'L', 'R', 'S'.
- Timeout de seguridad web: si pasa `X` ms sin comando web, la intención web vuelve a cero.
- Sumatoria de intenciones: `velocidad_final = intencion_joystick + intencion_web`.

#### [NEW] `esp32_server/boot.py`
- Configuración de red WiFi en modo Station (o AP) para MicroPython.

#### [NEW] `esp32_server/main.py`
- Servidor web asíncrono (`uasyncio`).
- Lógica para recibir peticiones en el endpoint `/api/command` y transmitir el comando `F,B,U,D,L,R,S` vía UART (GPIO 17) a 9600 bps.
- Endpoint `/` que sirve el archivo `index.html`.

#### [NEW] `esp32_server/index.html`
- Interfaz web minimalista pero moderna ("Control Remoto").
- Botones de control con uso de `fetch()` mediante JavaScript (eventos `mousedown`/`touchstart` para enviar comando y `mouseup`/`touchend` para enviar 'S').

#### [NEW] `openspec.md`
- Documento de especificación OpenSpec.
- Diagramas (o descripción) de la lógica de control.
- Especificación del protocolo UART y la API del servidor web.

## Verification Plan

### Manual Verification
1. Verificación de sintaxis de los archivos Python y Arduino.
2. Comprobación de que la arquitectura de pines en el código corresponde exactamente con la descrita en los requerimientos.
3. Generación del repositorio Github `PG_2526_Nombre_Apellido`.
