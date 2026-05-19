import uasyncio as asyncio
import machine
from machine import UART, Pin
import json

# Configuración de pines
LED = Pin(2, Pin.OUT)
# UART2 o UART1 (MicroPython ESP32 soporta UART 1 y 2). Usaremos UART 1 con TX en 17.
uart = UART(1, baudrate=9600, tx=17, rx=16)

# Función para leer el HTML
def get_html():
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except Exception as e:
        return "<h1>Error: index.html no encontrado</h1>"

# Enviar comando al Arduino vía UART
def send_uart_command(cmd):
    try:
        uart.write(cmd)
        print("Enviado:", cmd)
        # Parpadear LED de estado
        LED.value(1)
        # Utilizamos un pequeño timer no asíncrono para el LED, o simplemente lo dejamos encendido un momento
    except Exception as e:
        print("Error UART:", e)

# Handler de las peticiones HTTP
async def handle_client(reader, writer):
    LED.value(1)
    try:
        request_line = await reader.readline()
        if not request_line:
            return
        
        request_line = request_line.decode('utf-8').strip()
        print("Petición recibida:", request_line)
        
        # Ignorar headers restantes para simplificar
        while True:
            line = await reader.readline()
            if not line or line == b'\r\n':
                break
                
        # Parsear la petición
        if request_line.startswith('GET / HTTP'):
            html = get_html()
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n' + html
            writer.write(response.encode('utf-8'))
            await writer.drain()
            
        elif request_line.startswith('POST /api/command'):
            # En una petición POST básica sin Content-Length riguroso, 
            # leeremos un par de bytes o utilizaremos la URL para ser más seguros con MicroPython asíncrono,
            # pero dado que pedimos Fetch, leeremos el body.
            # NOTA: Para MicroPython es más seguro usar peticiones GET como /api/command?cmd=F
            pass
            
        elif request_line.startswith('GET /api/command?cmd='):
            # Extraer el comando de la URL
            cmd = request_line.split('cmd=')[1].split(' ')[0]
            if cmd in ['F', 'B', 'U', 'D', 'L', 'R', 'S']:
                send_uart_command(cmd)
                response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n{"status":"ok"}'
            else:
                response = 'HTTP/1.1 400 Bad Request\r\nConnection: close\r\n\r\n'
            
            writer.write(response.encode('utf-8'))
            await writer.drain()
            
        else:
            response = 'HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n'
            writer.write(response.encode('utf-8'))
            await writer.drain()
            
    except Exception as e:
        print("Error handle_client:", e)
    finally:
        writer.close()
        await writer.wait_closed()
        LED.value(0)

# Corutina principal
async def main():
    print("Iniciando servidor web asíncrono...")
    server = await asyncio.start_server(handle_client, '0.0.0.0', 80)
    
    while True:
        await asyncio.sleep(1)

# Iniciar loop
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Deteniendo...")
