## 1. Diseño de Estilos CSS (Modal en Schema.html)

- [ ] 1.1 Modificar las reglas CSS de `.modal-symbol-container` para permitir alturas dinámicas (`height: auto`, `min-height: 220px`) y aumentar el ancho máximo a `280px`.
- [ ] 1.2 Actualizar el título de la sección en el HTML de "Símbolo Esquemático" a "Esquema del Componente (Pinout)".
- [ ] 1.3 Asegurar que las etiquetas de texto de los pines dentro de los SVGs utilicen fuentes del sistema legibles (`Outfit` o `sans-serif`) y que se escalen de forma fluida.

## 2. Implementación de los SVG de Pinout (Base de Datos componentData)

- [ ] 2.1 Diseñar e inyectar el SVG de pinout para el **Arduino Nano**:
  - Representación de la placa con 15 pines en el lado izquierdo y 15 pines en el lado derecho.
  - Resaltar colores específicos para alimentación (`VIN`, `5V`, `3.3V`), tierras (`GND`), entradas analógicas (`A0`, `A1`, `A2`...) y pines lógicos de comunicación (`D12`, `D11`, etc.).
- [ ] 2.2 Diseñar e inyectar el SVG de pinout para el **ESP32 Gateway**:
  - Dibujo de los pines a los costados de la placa de desarrollo ESP32.
  - Rotular detalladamente `VIN`, `GND`, `TX2/G17`, `RX2/G16` y los pines de alimentación.
- [ ] 2.3 Diseñar e inyectar el SVG de pinout para el **TB6612FNG Driver**:
  - Representación del chip/módulo con sus pines rotulados a la izquierda y derecha.
  - Rotular las salidas de los motores (`AO1`/`AO2`, `BO1`/`BO2`, `CO1`/`CO2`) y las señales de control y potencia (`VM`, `VCC`, `PWMA/B/C`, `AIN1/2`, `BIN1/2`, `CIN1/2`, `STBY`).
- [ ] 2.4 Diseñar e inyectar el SVG de pinout para el **Joystick Físico**:
  - Módulo con el conector de 5 pines: `GND`, `+5V`, `VRx`, `VRy`, `SW`.
- [ ] 2.5 Diseñar e inyectar el SVG de pinout para los **Motores DC N20**:
  - Terminales de fuerza `M+` y `M-` y su correspondencia con las salidas del puente H.
- [ ] 2.6 Diseñar e inyectar el SVG de pinout para la **Fuente de Alimentación**:
  - Terminales de salida `+12V` y `GND` de potencia.

## 3. Pruebas y Ajustes de Visualización

- [ ] 3.1 Abrir `Schema.html` localmente y verificar el correcto centrado y escalado de cada pinout en resoluciones móviles y de escritorio.
- [ ] 3.2 Probar los temas Claro y Oscuro para verificar que el contraste de las etiquetas de pines y líneas sea el adecuado.
- [ ] 3.3 Validar que el modal se cierre correctamente y no conserve estados de imágenes previas.
