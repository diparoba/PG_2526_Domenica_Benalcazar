# OpenSpec: Sistema de Control de Grúa Torre Dual (Manual/Web)

## 1. Visión General
El sistema implementa un control dual para una grúa torre, permitiendo operar los ejes de rotación, elevación y traslado del carro mediante comandos manuales (joysticks) y comandos remotos a través de una interfaz web inalámbrica.

El hardware se basa en una arquitectura distribuida:
- **Controlador Principal (Arduino Nano):** Gestiona la lógica de hardware, actuadores y sensores en tiempo real.
- **Servidor de Interfaz (ESP32):** Sirve una interfaz web, recibe comandos de los usuarios vía HTTP y los retransmite al Nano por puerto serial.

## 2. Arquitectura de Hardware

### 2.1 Asignación de Pines - Arduino Nano (Actuador Principal)
| Componente / Función | Pines Utilizados | Detalles Técnicos |
| :--- | :--- | :--- |
| **Driver TB6612FNG** (Motores DC N20) | `AIN1`(D2), `AIN2`(D4), `PWMA`(D3) | Motor A (Carro) |
| | `BIN1`(D7), `BIN2`(D8), `PWMB`(D5) | Motor B (Elevación) |
| | `STBY` -> VCC | Habilitación continua |
| **Driver DRV8825** (Motor Nema 17) | `STEP`(D9), `DIR`(D10) | Eje Giro (Rotación Principal) |
| **Joysticks (Entradas Analógicas)** | `A0` (X), `A1` (Y), `A2` (Giro) | Resolución ADC: 10 bits (0-1023) |
| **Comunicación Serial UART** | `RX`(D0) | Conectado al TX del ESP32 |

### 2.2 Asignación de Pines - ESP32 (Servidor Web)
| Componente / Función | Pines Utilizados | Detalles Técnicos |
| :--- | :--- | :--- |
| **Comunicación Serial UART1** | `TX`(GPIO 17) | Conectado al RX del Nano (D0) |
| | `RX`(GPIO 16) | Opcional, para recibir feedback |
| **Status LED** | `GPIO 2` | Indicador de actividad de transmisión |

## 3. Protocolos de Comunicación

### 3.1 Protocolo Serial (UART)
- **Configuración:** 9600 baudios, 8 bits de datos, sin paridad, 1 bit de parada (8N1).
- **Dirección:** Simplex (ESP32 -> Arduino Nano).
- **Carga Útil (Payload):** Transmisión de caracteres individuales (1 byte) que representan una intención de movimiento.

**Mapeo de Comandos UART:**
- `F` (Forward): Mover carro hacia adelante.
- `B` (Backward): Mover carro hacia atrás.
- `U` (Up): Subir gancho.
- `D` (Down): Bajar gancho.
- `L` (Left): Girar grúa a la izquierda.
- `R` (Right): Girar grúa a la derecha.
- `S` (Stop): Detener todo movimiento comandado por la web.

### 3.2 Protocolo de API Web (HTTP RESTful)
El ESP32 expone un servidor web asíncrono básico en el puerto 80.

#### `GET /`
- **Descripción:** Sirve la interfaz gráfica principal (HTML, CSS, JS).
- **Respuesta:** `Content-Type: text/html` (Status: 200 OK).

#### `GET /api/command?cmd={char}`
- **Descripción:** Endpoint que recibe comandos asíncronos (Fetch API) desde el cliente web y desencadena una transmisión UART.
- **Parámetros:**
  - `cmd` (string): Debe ser un comando válido (`F`, `B`, `U`, `D`, `L`, `R`, `S`).
- **Respuesta Exitoso:** `{"status":"ok"}` (Status: 200 OK)
- **Respuesta Fallo:** Status: 400 Bad Request.

## 4. Lógica de Control (Firmware Arduino)

La lógica principal en el Arduino Nano emplea un sistema de "Sumatoria de Intenciones" que evalúa en cada ciclo las órdenes entrantes de las dos interfaces de control.

```text
velocidad_final = intencion_joystick + intencion_web
```

### 4.1 Tolerancias y Timeout de Seguridad
- **Dead-zone (Joystick):** Para evitar movimientos parásitos debido al ruido del ADC, se aplica una zona muerta en los valores centrales del joystick (480 a 540). Fuera de estos umbrales, el valor es mapeado al ciclo de trabajo de PWM o velocidad del Stepper.
- **Web Safety Timeout:** Todo comando UART diferente de 'S' (Stop) resetea un temporizador `lastWebCmdTime`. Si transcurren más de `500 ms` sin recibir un nuevo comando web (gracias a los envíos periódicos del cliente vía JS `setInterval`), las variables de `intencion_web` se anulan automáticamente a cero. Esto previene que la grúa siga moviéndose indefinidamente si se pierde la conexión WiFi o se cierra el navegador.

### 4.2 Control de Actuadores
- **Motores DC:** Usan PWM estándar de Arduino (0-255). Se determinan direcciones activando el pin `AIN1/BIN1` respectivo y desactivando el otro pin `AIN2/BIN2`.
- **Motor a Pasos:** Integrado con la librería `AccelStepper`. El Nano invoca `stepper.runSpeed()` constantemente en el `loop()` en función a la `velGiroFinal` calculada. No se emplean funciones bloqueantes como `delay()`.

## 5. Diseño de Interfaz de Usuario (UI)
La web implementa un diseño inspirado en el "Glassmorphism":
- **Colores:** Esquema oscuro (Fondo: `#0f172a`, Paneles translúcidos: `rgba(30, 41, 59, 0.7)`).
- **Responsive:** Adaptable para resoluciones móviles con prevención de `zoom` y `scroll` accidentales (CSS `touch-action: none`).
- **Interactividad:** Control fluido usando la API `fetch()`. Los eventos táctiles nativos (`touchstart`, `touchend`) y del mouse garantizan que la interacción refleje la sensación de presionar un botón de un control remoto físico.
