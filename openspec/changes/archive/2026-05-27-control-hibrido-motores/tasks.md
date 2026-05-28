## 1. Arduino Firmware (Control de Motores y Modos)

- [x] 1.1 Eliminar la importación y variables de `AccelStepper` de `grua_arduino/grua_arduino.ino`.
- [x] 1.2 Definir constantes de velocidad máxima `MAX_VEL_CARRO`, `MAX_VEL_ELEVACION` y `MAX_VEL_GIRO` en Arduino.
- [x] 1.3 Asignar pines físicos `CIN1` (D9), `CIN2` (D10) y `PWMC` (D6) para el canal del nuevo puente H (Giro).
- [x] 1.4 Configurar el pin `JOY_BTN_PIN` (D11) como `INPUT_PULLUP` para detectar la pulsación del botón.
- [x] 1.5 Crear la función de actuación de potencia `controlMotorC(int speed)` para regular el giro.
- [x] 1.6 Implementar lógica de alternancia de modo con antirrebote (debounce) en el bucle principal de Arduino.
- [x] 1.7 Modificar la mezcla de intenciones para que responda de forma exclusiva a Joysticks (Manual) o Web (Remoto) según el modo activo.
- [x] 1.8 Limitar el timeout de seguridad (Watchdog de 500ms) de modo que solo opere y detenga motores en el modo de control Web.

## 2. ESP32 Servidor y API

- [x] 2.1 Configurar el buffer UART en `esp32_server/main.py` y `esp32_server/telemetry.py` para lectura asíncrona de datos.
- [x] 2.2 Agregar variable global `modo_control_web` y su sincronización a través de lecturas serie (`W` y `M`).
- [x] 2.3 Implementar endpoint `GET /api/status` que devuelva el estado del modo en JSON.
- [x] 2.4 Implementar endpoint `GET /api/mode?set={web|manual}` que cambie el modo del ESP32 y lo transmita por serial.

## 3. Interfaz Web y Esquema Físico

- [x] 3.1 Agregar el interruptor (Toggle Switch CSS) de selección de modo en la cabecera de `esp32_server/index.html`.
- [x] 3.2 Añadir llamadas `fetch` en el frontend para enviar solicitudes al cambiar de modo en el Toggle Switch.
- [x] 3.3 Configurar el polling periódico (`setInterval` de 1000ms) al endpoint `/api/status` para alinear el estado del Toggle Switch en el navegador.
- [x] 3.4 Crear el archivo interactivo `Schema.html` en la raíz del proyecto para visualizar todas las conexiones electrónicas.
