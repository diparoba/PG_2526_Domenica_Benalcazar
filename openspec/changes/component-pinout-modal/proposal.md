## Why

Los usuarios de la interfaz de control de la grúa torre necesitan comprender no solo las conexiones simplificadas del diagrama interactivo general, sino también el esquema físico de pines (pinout) detallado de cada elemento al hacer clic en él. Esto facilita la verificación física del hardware, la depuración de conexiones defectuosas y el entendimiento didáctico del sistema electrónico completo.

## What Changes

- Rediseño del contenedor de símbolos en el modal interactivo de `Schema.html` para soportar esquemas de pinouts más detallados y verticales.
- Reemplazo de los símbolos esquemáticos básicos por diagramas SVG detallados, coloridos y con etiquetas de pinout para:
  - Arduino Nano (esquema de 30 pines).
  - ESP32 Gateway (esquema de pines WiFi/UART/Power).
  - Drivers TB6612FNG (pines VM, VCC, entradas y salidas de potencia).
  - Joysticks Físicos (conexiones GND, VCC, VRx, VRy, SW).
  - Motores DC N20 y Fuente de Alimentación de 12V.
- Actualización de los textos explicativos y especificaciones en la base de datos de componentes para reflejar detalladamente el conexionado de pines.

## Capabilities

### Modified Capabilities

- `electronic-schematic`: Se mejora el esquema electrónico interactivo (`Schema.html`) al proveer información visual técnica y precisa de los pines de conexión directamente en la interfaz.

## Impact

- **Frontend (`Schema.html`)**: Modificación del código CSS del modal (`.modal-symbol-container` y sus SVGs) y actualización de la estructura `componentData` en JavaScript. No hay impacto en la lógica de control del firmware de ESP32 o Arduino Nano.
