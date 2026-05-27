# Requisitos Técnicos para la Grúa Torre

## Resumen del Sistema
- **Control Dual**: Manual vía Joysticks y remoto vía web.
- **Comunicación**: UART (9600 bps) entre ESP32 (servidor web) y Arduino Nano (control de motores).

## Hardware
- **Arduino Nano**: Controlador principal de los motores.
  - *Drivers*: TB6612FNG (motores DC N20) y DRV8825 (motor paso a paso NEMA 17).
  - *Sensores*: Joysticks en ejes X, Y, Z (pines A0, A1, A2).
- **ESP32**: Servidor Wi‑Fi y puente UART.
  - *Wi‑Fi*: SSID y contraseña configurables en `boot.py`.
  - *UART*: TX0 ↔ RX0, 9600 bps.

## Pines Arduino Nano
| Función | Pin |
|---|---|
| Joystick X | A0 |
| Joystick Y | A1 |
| Joystick Z (giro) | A2 |
| Motor DC IN1 | 2 |
| Motor DC IN2 | 3 |
| Motor DC PWM | 5 |
| Stepper DIR | 6 |
| Stepper STEP | 7 |
| Stepper EN (DRV8825) | 8 |
| UART RX (recepción de ESP32) | 10 |
| UART TX (envío a ESP32) | 11 |

## Comunicación UART
- **Comandos desde ESP32 → Arduino** (un solo carácter):
  - `F` – Mover carro adelante.
  - `B` – Mover carro atrás.
  - `U` – Elevar.
  - `D` – Bajar.
  - `L` – Girar izquierda.
  - `R` – Girar derecha.
  - `S` – STOP (detener todos los motores).
- **Respuestas Arduino → ESP32** (opcional, para depuración):
  - `OK` – comando ejecutado.
  - `ERR` – error.

## Seguridad
- Timeout de 200 ms: si no se recibe un comando continuo, el Arduino debe ejecutar `S`.
- PWM limitado a 255 (full speed) y a 0 (detenido).

## Software
- **Arduino (C++)**: Lectura de joysticks, generación local de comandos y parser UART.
- **ESP32 (MicroPython)**: Conexión Wi‑Fi, servidor HTTP, UI web, envío de comandos UART.

## UI Web
- Botones para cada movimiento con eventos `mousedown`/`touchstart` → envío de comando, `mouseup`/`touchend` → envío de `S`.
- Diseño responsivo, modo claro/oscuro, tipografía *Outfit*.
