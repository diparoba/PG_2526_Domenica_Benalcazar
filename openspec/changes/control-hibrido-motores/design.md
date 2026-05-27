## Context

El sistema actual de control de grúa torre utiliza una arquitectura dual de hardware (ESP32 para la interfaz web de pasarela y Arduino Nano para el manejo directo de actuadores). La cinemática de giro utilizaba un motor a pasos controlado mediante la librería `AccelStepper` y pines `D9`/`D10`.
Con la sustitución del motor a pasos por un motorreductor DC de 30 RPM, el giro ahora se controla de la misma forma que el carro y la elevación, mediante señales de dirección y PWM.
Además, se requiere cambiar el modelo de "suma mixta" de entradas físicas y web por un modelo de "control exclusivo" alternable por hardware (botón del joystick) y software (switch web).

## Goals / Non-Goals

**Goals:**
- Sustituir la lógica de control del Stepper en Arduino por control de motor DC con PWM asignando pines libres (`D9`, `D10` de dirección y `D6` de PWM).
- Permitir la parametrización de velocidades máximas independientes (`MAX_VEL_*`) para cada motor DC en Arduino Nano.
- Sincronizar bidireccionalmente el modo de control (Web vs. Manual) entre ESP32 y Arduino Nano usando UART.
- Proporcionar un toggle de modo en la página de interfaz web (`index.html`) y un botón físico en el joystick (`D11`) para cambiar el modo.
- Crear un archivo interactivo `Schema.html` para la documentación del conexionado.

**Non-Goals:**
- No se modificará la estructura de red del ESP32 (mantiene el modo AP y uasyncio en puerto 80).
- No se agregará control de lazo cerrado (encoders) para los motores DC en esta fase.

## Decisions

### 1. Control del tercer motor de giro (DC vs. Stepper)
- **Decisión**: Se remueve el uso de `AccelStepper.h` y se implementa una función de control de puente H estándar para el Giro.
- **Pines**: Dirección en `D9` y `D10` (reutilizados) y PWM en el pin `D6` (nuevo pin libre con temporizador PWM).
- **Razón**: Permite la simplificación de hardware y unifica el modelo de programación de los tres motores.

### 2. Sincronización bidireccional del Modo de Control
- **Decisión**: Se implementa un modelo de paso de mensajes simples sobre el canal serial existente (Arduino $\leftrightarrow$ ESP32).
  - Arduino envía `W` (Web) o `M` (Manual) cuando cambia localmente por el botón físico.
  - ESP32 lee UART y actualiza su estado. Si el switch web es pulsado, ESP32 envía `W` o `M` al Arduino.
- **Razón**: Garantiza consistencia de la interfaz web y respuesta instantánea del botón físico sin requerir complejas librerías de comunicación.

### 3. Sincronización Web mediante Polling de Corta Duración
- **Decisión**: El cliente web de `index.html` realiza un `fetch('/api/status')` cada 1000ms para obtener el JSON del estado actual de la grúa.
- **Razón**: El uso de polling a 1 Hz es ligero para el servidor `uasyncio` del ESP32 y actualiza el switch de la interfaz de manera fluida si el operario presiona el botón físico.

## Risks / Trade-offs

- **[Riesgo] Tráfico de polling satura el servidor de ESP32** $\rightarrow$ *Mitigación*: Mantener el tiempo de polling en 1000ms o mayor, y asegurar que la respuesta del endpoint `/api/status` sea un JSON pequeño y pre-renderizado.
- **[Riesgo] Ruido de rebotes en el pin D11 (Botón)** $\rightarrow$ *Mitigación*: Implementar antirrebote por software en Arduino Nano usando un retardo no bloqueante con `millis() >= 50ms`.
