import network
import socket
import time
from machine import Pin, ADC

# =====================================================================
# 1. CONFIGURACIÓN DE PINES PARA EL RESPALDO FÍSICO (HÍBRIDO)
# =====================================================================
# Pines de ejemplo en el ESP32-S3 para botones o joysticks físicos por "cualquier cosa"
boton_emergencia_fisico = Pin(4, Pin.IN, Pin.PULL_UP) # Botón físico tipo E-STOP

# Si usan un joystick físico analógico (dos ejes: X para Giro, Y para Carro)
adc_giro_x = ADC(Pin(5))  
adc_carro_y = ADC(Pin(6))
adc_giro_x.atten(ADC.ATTEN_11DB) # Rango de voltaje completo (0-3.3V)
adc_carro_y.atten(ADC.ATTEN_11DB)

# Si usan botones simples para subir/bajar gancho físicamente
btn_subir_fisico = Pin(7, Pin.IN, Pin.PULL_UP)
btn_bajar_fisico = Pin(8, Pin.IN, Pin.PULL_UP)

# =====================================================================
# 2. ACTUADORES: FUNCIONES MODULARES DE MOVIMIENTO FÍSICO
# =====================================================================
def detener_todo():
    # Prioridad absoluta en el hardware
    pass

def mover_carro_adelante():
    pass

def mover_carro_atras():
    pass

def girar_derecha():
    pass

def girar_izquierda():
    pass

def subir_gancho():
    pass

def bajar_gancho():
    pass

# Enrutador cinemático unificado
def procesar_comando(cmd):
    if cmd == 'F': mover_carro_adelante()
    elif cmd == 'B': mover_carro_atras()
    elif cmd == 'R': girar_derecha()
    elif cmd == 'L': girar_izquierda()
    elif cmd == 'U': subir_gancho()
    elif cmd == 'D': bajar_gancho()
    elif cmd == 'S': detener_todo()

# =====================================================================
# 3. LECTURA DEL PANEL FÍSICO DE RESPALDO (HARDWARE)
# =====================================================================
def leer_mandos_fisicos():
    """
    Esta función revisa el estado de los componentes físicos.
    Si detecta acción física, genera un comando local.
    """
    # 1. Prioridad Máxima: Parada de emergencia física (PULL_UP lee 0 al presionar)
    if boton_emergencia_fisico.value() == 0:
        return 'S'
        
    # 2. Lectura de elevación física (Gancho)
    if btn_subir_fisico.value() == 0:
        return 'U'
    if btn_bajar_fisico.value() == 0:
        return 'D'

    # 3. Lectura de Joystick Analógico (Filtro de zona muerta física entre 1500 y 2500)
    val_x = adc_giro_x.read()
    val_y = adc_carro_y.read()
    
    # Evaluar prioridades de ejes (como en el control digital)
    if abs(val_x - 2048) > abs(val_y - 2048):
        if val_x > 2800: return 'R' # Giro Horario
        if val_x < 1200: return 'L' # Giro Antihorario
    else:
        if val_y > 2800: return 'F' # Carro Adelante
        if val_y < 1200: return 'B' # Carro Atrás
        
    return None # Si nadie está tocando los controles físicos

# =====================================================================
# 4. CONFIGURACIÓN DE RED (AP LOCAL)
# =====================================================================
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='Grua_Industrial_Control', password='PolitecnicaEPN')

# Configurar el socket del servidor de modo "No Bloqueante"
# Esto es vital para que el ESP32 no se quede congelado esperando la web 
# y pueda seguir leyendo los botones físicos al mismo tiempo.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
s.setblocking(False) 

print("\n=== SISTEMA HÍBRIDO OPERATIVO ===")
print("IP del servidor:", ap.ifconfig()[0])
print("==================================\n")

# =====================================================================
# 5. BUCLE PRINCIPAL DE CONTROL HÍBRIDO SIMULTÁNEO
# =====================================================================
ultimo_comando = 'S'

while True:
    comando_actual = None
    
    # --- FRENTE 1: Intentar leer si llegó algo desde la interfaz Web ---
    try:
        conn, addr = s.accept()
        request = conn.recv(1024).decode('utf-8')
        if request:
            first_line = request.split('\n')[0]
            if "/api/command?cmd=" in first_line:
                partes = first_line.split("cmd=")
                comando_actual = partes[1][0]
                
                # Responder rápido a la interfaz web para evitar lag
                conn.send('HTTP/1.1 200 OK\nContent-Type: text/plain\n\nOK')
        conn.close()
    except OSError:
        # No hay conexiones web entrantes en este instante, continúa sin trabarse
        pass

    # --- FRENTE 2: Si la web está en reposo, revisar los mandos físicos ---
    if comando_actual is None:
        comando_fisico = leer_mandos_fisicos()
        if comando_fisico is not None:
            comando_actual = comando_fisico
        else:
            # Si nadie interactúa ni por web ni por físico y el último comando no fue detenerse
            if ultimo_comando != 'S':
                comando_actual = 'S'

    # --- EJECUCIÓN UNIFICADA ---
    if comando_actual is not None and comando_actual != ultimo_comando:
        print(f"[HÍBRIDO] Cambio de estado a comando: {comando_actual}")
        procesar_comando(comando_actual)
        ultimo_comando = comando_actual
        
    time.sleep(0.02) # Ciclo de estabilidad para el procesador (20ms)