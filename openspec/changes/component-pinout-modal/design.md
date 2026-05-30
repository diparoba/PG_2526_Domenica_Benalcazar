## Context

El sistema de la grúa torre dispone de un esquema interactivo en `Schema.html` que describe las conexiones lógicas entre módulos mediante líneas de cables de colores. Al hacer clic en un componente, se despliega un modal con la imagen del dispositivo (de la carpeta `images/`) y un símbolo esquemático muy simplificado. El usuario desea que en lugar del símbolo simplificado, se muestre el esquema de cada elemento electrónico con su pinout detallado para identificar qué pines físicos específicos se conectan entre sí.

## Goals / Non-Goals

**Goals:**
- Modificar el diseño CSS del modal en `Schema.html` para permitir diagramas de pinout más grandes y legibles.
- Diseñar gráficos vectoriales SVG en línea para cada uno de los 6 tipos de componentes (Arduino Nano, ESP32, TB6612FNG, Joystick, Motor DC, Fuente).
- Cada SVG de pinout debe estar codificado por colores siguiendo un estándar común (Rojo: VCC, Negro/Gris: GND, Azul: Señales Analógicas, Púrpura: PWM, Verde: Señales Digitales, Amarillo: UART).

**Non-Goals:**
- No se creará ninguna imagen PNG o JPG externa nueva; los pinouts se generarán dinámicamente como gráficos vectoriales SVG embebidos en el código JavaScript (`componentData`).
- No se altera la lógica de comunicaciones ni de control en ESP32 ni en Arduino Nano.

## Decisions

### 1. Reutilización de `.modal-symbol-container`
- **Decisión**: Se conservará el contenedor existente pero se renombrará semánticamente a nivel de CSS y visualización. Se cambiará el título de "Símbolo Esquemático" a "Esquema de Pines (Pinout)" y se incrementará su altura permitida a `auto` con un `min-height: 220px` para dar cabida a los pines de Arduino Nano y ESP32.
- **Razón**: Evita reescribir la estructura HTML del modal y mantiene la compatibilidad con el sistema de temas (Claro/Oscuro) ya implementado.

### 2. Formato de los Pinouts (SVG Inline)
- **Decisión**: Implementar los pinouts como SVGs interactivos de alta calidad embebidos directamente en las propiedades `symbol` de `componentData` en JavaScript.
- **Razón**: Permite escalabilidad y renderizado perfecto en cualquier resolución sin dependencias de red adicionales, y se adapta de forma nativa a los estilos CSS del tema activo.

### 3. Codificación de Colores Estándar
- **Decisión**: Usar un sistema uniforme de colores para el contorno de los pines y sus etiquetas:
  - Alimentación Lógica/Potencia (VCC/VIN): `#ef4444` (Rojo) o `#f97316` (Naranja)
  - Tierra (GND): `#64748b` (Gris) o `#475569` (Gris Oscuro)
  - Pines Analógicos (A0-A7): `#3b82f6` (Azul)
  - Pines PWM / Control: `#a855f7` (Morado)
  - Pines UART: `#eab308` (Amarillo)
  - Pines Digitales Genéricos: `#10b981` (Verde)

## Risks / Trade-offs

- **[Riesgo] El modal se vuelve muy alto y desborda pantallas pequeñas** $\rightarrow$ *Mitigación*: Utilizar flexbox y scroll interno en la caja del modal para pantallas móviles. Los SVG de pinout deben tener una relación de aspecto flexible y escalar con `max-height` proporcional.
