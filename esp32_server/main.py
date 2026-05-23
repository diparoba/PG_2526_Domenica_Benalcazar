import uasyncio as asyncio
from machine import UART, Pin, ADC
import ujson

# 1. Configuración de Hardware
uart = UART(1, baudrate=9600, tx=17, rx=16)
boton_emergencia = Pin(4, Pin.IN, Pin.PULL_UP)
btn_subir = Pin(7, Pin.IN, Pin.PULL_UP)
btn_bajar = Pin(8, Pin.IN, Pin.PULL_UP)
adc_giro = ADC(Pin(5)); adc_giro.atten(ADC.ATTEN_11DB)
adc_carro = ADC(Pin(6)); adc_carro.atten(ADC.ATTEN_11DB)

# Variables globales
logs = ["Sistema Híbrido Iniciado"]
comando_web = 'S'
ultimo_comando_enviado = 'S'

# 2. Funciones de Telemetría
def log_event(msg):
    global logs
    logs.append(msg)
    if len(logs) > 6: logs.pop(0)

# 3. Lógica de lectura de mandos físicos (Respaldo)
def leer_mandos_fisicos():
    if boton_emergencia.value() == 0: return 'S'
    if btn_subir.value() == 0: return 'U'
    if btn_bajar.value() == 0: return 'D'
    
    val_x = adc_giro.read()
    val_y = adc_carro.read()
    
    if abs(val_x - 2048) > 800: return 'R' if val_x > 2800 else 'L'
    if abs(val_y - 2048) > 800: return 'F' if val_y > 2800 else 'B'
    return None

# 4. Servidor Web Asíncrono
async def handle_client(reader, writer):
    global comando_web
    request = (await reader.readline()).decode('utf-8')
    while await reader.readline() != b'\r\n': pass

    if "/api/command?cmd=" in request:
        comando_web = request.split("cmd=")[1][0]
        writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK")
    elif "/api/logs" in request:
        writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + ujson.dumps(logs).encode())
    else:
        with open('index.html', 'r') as f:
            writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + f.read().encode())
    await writer.drain()
    writer.close()

# 5. Bucle de Control Híbrido (El corazón del sistema)
async def control_loop():
    global ultimo_comando_enviado
    while True:
        # Prioridad: Si Web no está en 'S', usamos Web. Si Web es 'S', usamos físico.
        cmd_a_enviar = comando_web if comando_web != 'S' else (leer_mandos_fisicos() or 'S')
        
        if cmd_a_enviar != ultimo_comando_enviado:
            uart.write(cmd_a_enviar)
            log_event(f"Estado: {cmd_a_enviar}")
            ultimo_comando_enviado = cmd_a_enviar
            
        await asyncio.sleep(0.05) # Ciclo de 50ms (muy rápido y estable)

# 6. Ejecución
async def main():
    asyncio.create_task(asyncio.start_server(handle_client, "0.0.0.0", 80))
    await control_loop()

asyncio.run(main())