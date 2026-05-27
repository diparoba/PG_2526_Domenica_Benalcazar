## Context

El ESP32 experimenta inestabilidades de memoria al procesar peticiones HTTP de control web concurrentes mientras sirve la interfaz pesada.
Para resolverlo, se propone separar físicamente el canal de control y depuración:
1. **Control Principal**: La interfaz web (`index.html`) se ejecuta localmente y se conecta directamente al Arduino Nano por cable USB usando la **Web Serial API**.
2. **Depuración Inalámbrica**: El Arduino envía logs de depuración mediante **SoftwareSerial** (pin D12 TX) al ESP32. El ESP32 los acumula y los sirve en una página HTML de logs ultraliviana (estilo terminal retro con refresco de 2s) en el puerto 80.

## Goals / Non-Goals

**Goals:**
- Implementar la Web Serial API nativa en `index.html` para la conexión directa USB-Serial.
- Integrar la librería `SoftwareSerial` en Arduino Nano para la salida secundaria de logs (pines D13 RX, D12 TX).
- Modificar el script de ESP32 MicroPython (`main.py`) para actuar únicamente como un receptor serie y servidor de logs ultraliviano.
- Reorganizar el repositorio en las carpetas `/arduino/`, `/esp32/` y `/web_server/`, eliminando copias de la raíz.
- Agregar enlaces de navegación cruzada en `index.html` y `Schema.html`.

**Non-Goals:**
- No se modificará el cableado de potencia ni la lógica cinemática del Arduino para el control de los tres motores.
- No se añadirá comunicación inalámbrica de control (WebSockets/fetch) como canal primario (se relega a fallback).

## Decisions

### 1. Web Serial API sobre Puerto USB
- **Decisión**: Usar la API de puerto serie del navegador para abrir el puerto a 9600 bps.
- **Razón**: Permite latencia mínima en comandos, procesamiento local de telemetría y elimina la carga de procesamiento del ESP32.

### 2. SoftwareSerial para Canal Secundario de Logs
- **Decisión**: Crear una instancia `SoftwareSerial debugSerial(13, 12);` en Arduino. Conectar el pin D12 (TX) al pin RX2 (GPIO 16) del ESP32.
- **Razón**: El puerto serie por hardware (USB) está reservado para el control e intercambio de JSON con la laptop. El canal secundario de SoftwareSerial aísla los mensajes de texto plano.

### 3. Servidor de Logs en ESP32 MicroPython
- **Decisión**: Rediseñar `main.py` de ESP32 para leer UART, guardar hasta 50 líneas en una lista circular y servirlas en una plantilla HTML minimalista con `<meta http-equiv="refresh" content="2">`.
- **Razón**: Evita el desbordamiento de memoria (OutOfMemory) y simplifica el servidor al eliminar todos los endpoints REST interactivos de control.

### 4. Estructura de Carpetas Limpia
- **Decisión**: Agrupar los ficheros de la siguiente manera:
  - `/arduino/grua_arduino/grua_arduino.ino`
  - `/esp32/boot.py`, `/esp32/main.py`
  - `/web_server/index.html`, `/web_server/Schema.html`
- **Razón**: Facilita el mantenimiento, despliegue y evita archivos huérfanos en la raíz del proyecto.

## Risks / Trade-offs

- **[Riesgo] Falta de soporte de Web Serial API** $\rightarrow$ *Mitigación*: Mantener el sistema de llamadas HTTP `fetch` tradicional en `index.html` como fallback si `navigator.serial` no está definido.
- **[Riesgo] Pérdida de rendimiento en SoftwareSerial** $\rightarrow$ *Mitigación*: Utilizar una velocidad estándar y baja de 9600 bps para evitar colisiones e interrupciones en el lazo principal de Arduino Nano.
