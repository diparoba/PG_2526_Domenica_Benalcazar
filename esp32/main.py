import uasyncio as asyncio
from machine import UART, Pin

# Configuración de Hardware
# UART1 con TX=17 y RX=16 a 9600 bps para recibir logs del Arduino (RX=16)
uart = UART(1, baudrate=9600, tx=17, rx=16)

# Buffer circular de 50 líneas
logs = ["LOG MONITOR INICIADO"]

def add_log(line):
    global logs
    line = line.strip()
    if line:
        logs.append(line)
        if len(logs) > 50:
            logs.pop(0)

# Tarea asíncrona para leer líneas de UART
async def leer_uart_task():
    print("Iniciando tarea de lectura UART1...")
    buffer = b""
    while True:
        if uart.any() > 0:
            try:
                # Leer bytes disponibles
                chunk = uart.read(uart.any())
                if chunk:
                    buffer += chunk
                    # Procesar líneas completas
                    while b"\n" in buffer:
                        linea_bytes, buffer = buffer.split(b"\n", 1)
                        linea_str = linea_bytes.decode('utf-8', 'ignore').strip()
                        if linea_str:
                            add_log(linea_str)
                            print(f"[UART LOG] {linea_str}")
            except Exception as e:
                print("Error en lectura UART:", e)
        await asyncio.sleep_ms(50)

# Servidor Web asíncrono
async def handle_client(reader, writer):
    try:
        request_line = await reader.readline()
        if not request_line:
            return
        
        request_str = request_line.decode('utf-8').strip()
        # Consumir el resto de las cabeceras HTTP
        while True:
            line = await reader.readline()
            if not line or line == b'\r\n':
                break
                
        if request_str.startswith("GET / HTTP"):
            # Generar página HTML retro de terminal
            html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="2">
    <title>Terminal de Depuración Inalámbrica</title>
    <style>
        body {
            background-color: #000000;
            color: #4ade80;
            font-family: 'Courier New', Courier, monospace;
            padding: 20px;
            margin: 0;
            font-size: 14px;
            line-height: 1.6;
        }
        .terminal {
            border: 2px solid #333;
            border-radius: 8px;
            padding: 15px;
            background-color: #050505;
            box-shadow: 0 0 15px rgba(74, 222, 128, 0.2);
            max-width: 800px;
            margin: 0 auto;
        }
        .header {
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            font-weight: bold;
            color: #22c55e;
        }
        .log-list {
            list-style: none;
            padding: 0;
            margin: 0;
            height: 400px;
            overflow-y: auto;
        }
        .log-item {
            margin-bottom: 6px;
            white-space: pre-wrap;
            border-left: 3px solid #15803d;
            padding-left: 8px;
        }
        .blink {
            animation: blinker 1s linear infinite;
        }
        @keyframes blinker {
            50% { opacity: 0; }
        }
    </style>
</head>
<body>
    <div class="terminal">
        <div class="header">
            <span>📟 MONITOREO DE GRÚA TORRE - ESP32</span>
            <span class="blink">● EN VIVO</span>
        </div>
        <div class="log-list">
"""
            for log in logs:
                html += f'            <div class="log-item">{log}</div>\n'
                
            html += """        </div>
    </div>
</body>
</html>"""
            
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n' + html
            writer.write(response.encode('utf-8'))
            await writer.drain()
        else:
            response = 'HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n'
            writer.write(response.encode('utf-8'))
            await writer.drain()
            
    except Exception as e:
        print("Error en handle_client:", e)
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    print("Iniciando monitor de depuracion inalambrica...")
    # Levantar el servidor web asíncrono
    server = await asyncio.start_server(handle_client, '0.0.0.0', 80)
    print("Servidor web escuchando en puerto 80.")
    
    # Levantar la tarea de lectura UART
    asyncio.create_task(leer_uart_task())
    
    # Bucle infinito para mantener el loop de asyncio corriendo
    while True:
        await asyncio.sleep(1)

# Arrancar el bucle asíncrono
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Servidor web apagado.")