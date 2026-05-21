import network
import time
import sys
import uselect

SSID = "WIFI_GRUA"
PASSWORD = "password123"

def connect_wifi(ssid, password):
    print("Iniciando configuracion WiFi...")
    # Configurar como Station (conectarse a un router)
    # Si deseas que la grúa cree su propia red, cambia a network.AP_IF
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"Conectando a {ssid}...")
        wlan.connect(ssid, password)
        
        # Esperar hasta conectar (timeout de 10 segundos)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print(".", end="")
            
    if wlan.isconnected():
        print("\nConexion exitosa!")
        print("IP Config:", wlan.ifconfig())
    else:
        print("\nError: No se pudo conectar al WiFi.")
        # Opcional: Levantar AP de emergencia aquí si falla la conexión STA

def menu_inicio(timeout_segundos=5):
    """
    Muestra un menú en la terminal. Avanza automáticamente si no hay respuesta.
    """
    print("\n" + "="*40)
    print("      SISTEMA DE CONTROL - GRÚA TORRE")
    print("="*40)
    print("1. Iniciar sistema normalmente (Modo Ejecución)")
    print("2. Detener en modo programación (Liberar REPL)")
    print(f"Selecciona una opción (Avanza a opción 1 en {timeout_segundos}s)...")
    
    # Configurar la terminal para escuchar la entrada del usuario sin bloquear
    poller = uselect.poll()
    poller.register(sys.stdin, uselect.POLLIN)
    
    tiempo_inicio = time.time()
    while (time.time() - tiempo_inicio) < timeout_segundos:
        # Revisar si hay datos en la terminal (espera hasta 100ms por ciclo)
        if poller.poll(100):
            caracter = sys.stdin.read(1)
            if caracter == '1':
                print("\n-> Opción 1 seleccionada. Iniciando...")
                return True
            elif caracter == '2':
                print("\n-> Opción 2 seleccionada. Modo programación activo.")
                print("Consola REPL liberada. Puedes subir o modificar archivos.")
                return False
    
    # Si se agota el tiempo sin respuesta, asumimos que está corriendo en la grúa de forma autónoma
    print("\n-> Tiempo de espera agotado. Iniciando de forma automática...")
    return True

# --- FLUJO DE INICIO ---

# Ejecutamos el menú ANTES de conectar al WiFi o cargar el main
if menu_inicio(timeout_segundos=5):
    # Si elige 1 o se agota el tiempo, conecta a WiFi y avanza a main.py
    connect_wifi(SSID, PASSWORD)
else:
    # Si elige 2, forzamos la detención del script del sistema operativo
    # Esto evita que MicroPython salte automáticamente a ejecutar el main.py
    sys.exit()
