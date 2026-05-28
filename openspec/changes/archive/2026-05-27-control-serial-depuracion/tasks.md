## 1. Directorios y Organización de Archivos

- [x] 1.1 Crear las carpetas de subsistemas `/arduino/grua_arduino/`, `/esp32/` y `/web_server/`
- [x] 1.2 Mover el firmware del microcontrolador principal `grua_arduino.ino` a `/arduino/grua_arduino/`
- [x] 1.3 Mover los archivos de ESP32 MicroPython `boot.py` y `main.py` a `/esp32/`
- [x] 1.4 Mover los archivos frontend `index.html` y `Schema.html` a `/web_server/`
- [x] 1.5 Eliminar las copias obsoletas o duplicadas de la raíz (incluyendo `telemetry.py`) para evitar archivos huérfanos


## 2. Firmware de Arduino Nano (Microcontrolador Principal)

- [x] 2.1 Importar `SoftwareSerial` y declarar la instancia `debugSerial(13, 12)` para la transmisión de logs
- [x] 2.2 Inicializar `debugSerial` a 9600 bps en `setup()` e implementar mensajes de log descriptivos para cada evento
- [x] 2.3 Redirigir todas las salidas textuales de logs y alertas hacia `debugSerial` en lugar de `Serial`
- [x] 2.4 Habilitar la escucha de comandos directos de un solo caracter ('F', 'B', 'U', 'D', 'L', 'R', 'S', 'W', 'M') desde el hardware `Serial` (USB)
- [x] 2.5 Implementar transmisión periódica (ej. cada 100ms) de la telemetría en formato JSON `{"giro": angle, "carro": position, "gancho": depth}` por el puerto `Serial` (USB)
- [x] 2.6 Reforzar el perro guardián de seguridad (Watchdog) que resetea las intenciones web si transcurren más de 500ms sin recibir comandos en modo Web


## 3. Firmware de ESP32 (MicroPython - Depuración Inalámbrica)

- [x] 3.1 Configurar `UART1` (TX=17, RX=16) a 9600 bps para recibir únicamente los logs del Arduino
- [x] 3.2 Implementar un buffer circular de logs de tipo lista en RAM que almacene estrictamente las últimas 50 líneas recibidas
- [x] 3.3 Crear una tarea asíncrona dedicada que lea continuamente de `UART1` y actualice el buffer circular de logs
- [x] 3.4 Configurar el servidor web minimalista usando sockets en el puerto 80 que responda a la ruta `/`
- [x] 3.5 Diseñar el HTML retornado para la terminal con estética retro (fondo negro, texto verde monocromo) y cabecera de autorefresco cada 2 segundos
- [x] 3.6 Limpiar `main.py` de toda lógica de control obsoleta, endpoints de la API (`/api/command`, `/api/status`, etc.) e hilos innecesarios para garantizar la estabilidad de memoria


## 4. Interfaz Web de Control (`index.html`)

- [x] 4.1 Incorporar un botón e interfaz de conexión usando la Web Serial API nativa de Chrome/Edge a 9600 bps
- [x] 4.2 Añadir escuchas de teclado (listeners) para que las teclas correspondientes envíen caracteres de control directo por el puerto serie
- [x] 4.3 Implementar lectura asíncrona del puerto serie USB en JavaScript, procesando las tramas JSON de telemetría y actualizando instantáneamente los SVGs y las gráficas
- [x] 4.4 Conservar el sistema de llamadas HTTP `fetch` original únicamente como fallback alternativo si no se inicia la conexión Web Serial
- [x] 4.5 Añadir la barra superior o cabecera con enlaces de navegación interactiva y simétrica para saltar a `Schema.html`


## 5. Diagrama de Conexiones (`Schema.html`)

- [x] 5.1 Actualizar el esquema SVG sustituyendo las conexiones UART bidireccionales previas por la línea de SoftwareSerial de Arduino D12 (TX) al pin RX2 (G16) de ESP32
- [x] 5.2 Modificar los textos informativos e interactivos en el SVG y la tabla de conexiones para detallar la función de SoftwareSerial (Logs)
- [x] 5.3 Añadir la cabecera con enlaces de navegación interactiva y simétrica para volver a `index.html`


## 6. Verificación e Integración

- [x] 6.1 Compilar y validar el código de Arduino Nano libre de errores
- [x] 6.2 Verificar sintácticamente el script `main.py` de ESP32
- [x] 6.3 Validar el funcionamiento del esquema y la interfaz en un navegador Chrome o Edge
- [x] 6.4 Ejecutar validaciones finales y archivar el cambio con `openspec archive`

