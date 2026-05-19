# Grúa Torre - Proyecto de Grado 🏗️🐉

Este documento explica de forma detallada y sencilla cómo funciona el código de la Grúa Torre controlada por WiFi. Te servirá como guía de estudio para defender tu proyecto de grado con total seguridad.

El sistema completo se compone de dos partes principales: 
1. **Un servidor web** alojado en el microcontrolador **ESP32**.
2. **Un controlador de motores** (tu Arduino) que recibe órdenes del ESP32.

A continuación, explicamos cada archivo del ESP32:

---

## 1. `boot.py` (La Conexión a Internet)
Este archivo es el primero que se ejecuta al encender el ESP32. Su único propósito es conectar el dispositivo a una red WiFi.

### ¿Cómo funciona?
*   **`network.WLAN(network.STA_IF)`**: Configura la antena del ESP32 en modo "Estación" (Station). Esto significa que el ESP32 no crea su propia red, sino que busca un router (como el de tu casa o los datos compartidos de tu celular) para conectarse.
*   **`wlan.connect(SSID, PASSWORD)`**: Utiliza el nombre de red y la contraseña configurados al inicio del archivo para intentar conectarse.
*   **El bucle `while`**: El código hace una pausa de máximo 10 segundos, esperando a que el router le asigne una dirección IP. Si tiene éxito, imprime la IP (que es la que escribes en el navegador web para entrar).

---

## 2. `main.py` (El Cerebro y el Servidor Web)
Una vez conectado al WiFi, se ejecuta `main.py`. Este archivo levanta una página web asíncrona y gestiona la comunicación serial (UART) con el Arduino.

### Conceptos Clave:
*   **`uasyncio` (Programación Asíncrona)**: El servidor web usa "asyncio", lo que permite que el ESP32 pueda atender a la página web y procesar comandos de forma paralela sin quedarse "trabado" o colgado.
*   **`uart = UART(1, baudrate=9600, ...)`**: Configura la comunicación Serial. El ESP32 se conecta al Arduino a través de dos pines (TX y RX) a una velocidad de 9600 bits por segundo.
*   **`send_uart_command(cmd)`**: Toma una letra (ej. `'F'` para Front/Avanzar, o `'S'` para Stop/Detener) y la envía por el cable al Arduino. Además, enciende el LED interno de la placa para indicarte visualmente que mandó el dato.

### Manejo de Peticiones (`handle_client`):
Cuando tu teléfono entra a la IP del ESP32, suceden dos cosas dependiendo de lo que el teléfono pida:
1.  **Pide la página web (`GET / HTTP`)**: El ESP32 lee el archivo `index.html` y se lo envía al teléfono. Así es como ves los botones.
2.  **Presionas un botón (`GET /api/command?cmd=X`)**: El teléfono hace una petición invisible indicando qué botón pulsaste. El ESP32 extrae la letra del comando (por ejemplo `cmd=U` para Subir el gancho), valida que sea una letra permitida, y llama a la función `send_uart_command()` para que el Arduino mueva el motor.

---

## 3. `index.html` (La Interfaz Gráfica "Cómo entrenar a tu dragón")
Este archivo es lo que el usuario final ve. Combina tres lenguajes: HTML (estructura), CSS (diseño) y JavaScript (lógica de los botones).

### El Diseño (CSS):
*   **Tema "Cómo entrenar a tu Dragón"**: Se diseñó con colores inspirados en Chimuelo (Toothless). El fondo es oscuro y texturizado como la noche y sus escamas, los botones y acentos brillan con un color verde-amarillo intenso (como los ojos del dragón), y el botón de emergencia tiene un acento rojo (inspirado en la aleta roja de su cola).
*   **Glassmorphism**: Los paneles de control parecen de cristal oscuro translúcido gracias a los filtros de desenfoque (`backdrop-filter: blur`).

### La Lógica (JavaScript):
*   **Eventos Táctiles (`touchstart`, `touchend`)**: Los botones están programados para reaccionar al tacto. Cuando pones el dedo en un botón (ej. "Subir"), envía el comando `'U'`.
*   **Seguridad Ante Todo**: En el instante en el que levantas el dedo de la pantalla (`touchend`), JavaScript envía automáticamente el comando `'S'` (Stop). Esto garantiza que la grúa nunca se quede moviéndose sola si sueltas el teléfono o te distraes, funcionando como un "hombre muerto" (deadman switch) de seguridad.
*   **`fetch()`**: Es la función moderna que envía los comandos al ESP32 de fondo, permitiendo que la página nunca tenga que recargarse mientras controlas la grúa.
