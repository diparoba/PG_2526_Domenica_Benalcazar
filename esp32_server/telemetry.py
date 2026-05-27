# ==========================================================
# ARCHIVO: main.py
# DESCRIPCIÓN: Cerebro Asíncrono Híbrido (Web + Consola UART)
# ==========================================================
import uasyncio as asyncio
import machine
from machine import UART, Pin
import json
import telemetry
import sys
import uselect

# Configuración del hardware
LED = Pin(2, Pin.OUT)
# UART1 con TX=17 y RX=16 para enviar comandos directos a los motores en el Arduino
uart = UART(1, baudrate=9600, tx=17, rx=16)
modo_control_web = False

def get_html():
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except Exception:
        return "<h1>Error: index.html no encontrado en la placa</h1>"

def send_uart_command(cmd):
    """Manda la letra de acción directo al Arduino de la maqueta"""
    global modo_control_web
    if not modo_control_web and cmd != 'S':
        # En modo manual, no enviamos comandos de movimiento ordinarios
        return
    try:
        uart.write(cmd)
        print(f"\n[UART] Mandado a motores: {cmd}")
        try:
            telemetry.log_event('uart_send', {'cmd': cmd})
        except Exception:
            pass
        LED.value(1) # Prende el LED de estado al enviar
    except Exception as e:
        print("Error UART:", e)
        try:
            telemetry.log_event('error', {'where': 'send_uart_command', 'error': str(e)})
        except Exception:
            pass

async def handle_client(reader, writer):
    """Procesa las solicitudes web de tu amigo y tu D-Pad"""
    LED.value(1)
    try:
        request_line = await reader.readline()
        if not request_line:
            return
        
        request_line = request_line.decode('utf-8').strip()
        print("\nPetición web recibida:", request_line)
        
        try:
            telemetry.log_event('http_request', {'request_line': request_line})
        except Exception:
            pass
        
        # Ignorar los headers HTTP sobrantes
        while True:
            line = await reader.readline()
            if not line or line == b'\r\n':
                break
                
        # Enrutar peticiones
        if request_line.startswith('GET / HTTP'):
            html = get_html()
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n' + html
            writer.write(response.encode('utf-8'))
            await writer.drain()
            
        elif request_line.startswith('GET /api/command?cmd='):
            cmd = request_line.split('cmd=')[1].split(' ')[0]
            if cmd in ['F', 'B', 'U', 'D', 'L', 'R', 'S']:
                send_uart_command(cmd)
                try:
                    telemetry.log_event('command_received', {'cmd': cmd})
                except Exception:
                    pass
                response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n{"status":"ok"}'
            else:
                response = 'HTTP/1.1 400 Bad Request\r\nConnection: close\r\n\r\n'
            
            writer.write(response.encode('utf-8'))
            await writer.drain()
            sys.stdout.write("Escribe un comando manual: ")

        elif request_line.startswith('GET /api/status'):
            try:
                logs_text = ""
                try:
                    logs_text = telemetry.read_all()
                except Exception:
                    pass
                status_data = {"mode": "web" if modo_control_web else "manual", "logs": logs_text.split('\n')}
                response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n' + json.dumps(status_data)
            except Exception as ex:
                response = 'HTTP/1.1 500 Internal Error\r\nConnection: close\r\n\r\n'
            writer.write(response.encode('utf-8'))
            await writer.drain()
            sys.stdout.write("Escribe un comando manual: ")

        elif request_line.startswith('GET /api/mode?set='):
            mode_param = request_line.split('set=')[1].split(' ')[0].strip()
            if mode_param == "web":
                modo_control_web = True
                try:
                    uart.write(b"W")
                    telemetry.log_event('mode_change', {'mode': 'web', 'source': 'web_api'})
                except Exception:
                    pass
            elif mode_param == "manual":
                modo_control_web = False
                try:
                    uart.write(b"M")
                    telemetry.log_event('mode_change', {'mode': 'manual', 'source': 'web_api'})
                except Exception:
                    pass
            status_data = {"status": "ok", "mode": "web" if modo_control_web else "manual"}
            response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n' + json.dumps(status_data)
            writer.write(response.encode('utf-8'))
            await writer.drain()
            sys.stdout.write("Escribe un comando manual: ")

        elif request_line.startswith('GET /api/telemetry'):
            try:
                logs = telemetry.read_all()
                response = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\n' + logs
            except Exception:
                response = 'HTTP/1.1 500 Internal Error\r\nConnection: close\r\n\r\n'
            writer.write(response.encode('utf-8'))
            await writer.drain()
            sys.stdout.write("Escribe un comando manual: ")
            
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

async def escuchar_consola():
    """Monitorea Thonny sin trabar la página de red"""
    spoll = uselect.poll()
    spoll.register(sys.stdin, uselect.POLLIN)
    
    # Soporte híbrido para palabras completas o letras mayúsculas
    diccionario = {
        "subir": "U", "bajar": "D", "parar": "S",
        "frente": "F", "atras": "B", "izquierda": "L", "derecha": "R"
    }
    
    sys.stdout.write("Escribe un comando manual: ")
    while True:
        if spoll.poll(0):
            entrada = sys.stdin.readline().lower().strip()
            if entrada in diccionario:
                send_uart_command(diccionario[entrada])
            elif entrada.upper() in ['F', 'B', 'U', 'D', 'L', 'R', 'S']:
                send_uart_command(entrada.upper())
            else:
                print(f">> Comando '{entrada}' no válido.")
            
            sys.stdout.write("Escribe un comando manual: ")
        
        await asyncio.sleep_ms(80)

async def leer_uart():
    global modo_control_web
    while True:
        if uart.any() > 0:
            try:
                data = uart.read(1).decode('utf-8')
                if data == 'W':
                    modo_control_web = True
                    print("\n[UART] Modo cambiado a WEB (físico)")
                    try:
                        telemetry.log_event('mode_change', {'mode': 'web', 'source': 'physical'})
                    except Exception:
                        pass
                elif data == 'M':
                    modo_control_web = False
                    print("\n[UART] Modo cambiado a MANUAL (físico)")
                    try:
                        telemetry.log_event('mode_change', {'mode': 'manual', 'source': 'physical'})
                    except Exception:
                        pass
                sys.stdout.write("Escribe un comando manual: ")
            except Exception as e:
                print("Error leyendo UART:", e)
        await asyncio.sleep_ms(50)

async def main():
    print("\n" + "="*45)
    print("      SISTEMA ASÍNCRONO DE GRÚA - ACTIVO")
    print("="*45)
    print("Arrancando el servidor local de red (Puerto 80)...")
    
    await asyncio.start_server(handle_client, '0.0.0.0', 80)
    print("[OK] Servidor listo para recibir a la página web.")
    print("-" * 45)
    
    asyncio.create_task(escuchar_consola())
    asyncio.create_task(leer_uart())
    
    while True:
        await asyncio.sleep(1)

# Arrancar el bucle asíncrono robusto
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nServidor web apagado desde Thonny.")