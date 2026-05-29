# ==========================================================
# ARCHIVO: boot.py
# DESCRIPCIÓN: Menú de inicio interactivo con Timeout + WiFi
# ==========================================================
import sys
import uselect
import time
import network

def menu_inicio(timeout_segundos=5):
    """
    Muestra un menú en la terminal. Avanza automáticamente si no hay respuesta.
    """
    print("\n" + "="*40)
    print("      SISTEMA DE CONTROL - GRÚA TORRE")
    print("="*40)
    print("1. Iniciar sistema normalmente (Modo Ejecución)")
    print("2. Detener en modo programación (Liberar REPL)")
    print(f"Selecciona una opción (Avanza de forma automática en {timeout_segundos}s)...")
    
    # Configurar la terminal para escuchar la entrada sin bloquear
    poller = uselect.poll()
    poller.register(sys.stdin, uselect.POLLIN)
    
    tiempo_inicio = time.time()
    while (time.time() - tiempo_inicio) < timeout_segundos:
        if poller.poll(100):
            caracter = sys.stdin.read(1)
            if caracter == '1':
                print("\n-> Opción 1 seleccionada. Iniciando...")
                return True
            elif caracter == '2':
                print("\n-> Opción 2 seleccionada. Modo programación activo.")
                print("Consola REPL liberada. Puedes modificar tus archivos tranquilamente.")
                return False
    
    print("\n-> Tiempo de espera agotado. Iniciando de forma automática...")
    return True

def conectar_wifi_interactivo():
    wlan = network.WLAN(network.STA_IF)
    
    # Forzamos un reset del hardware WiFi para evitar el "Internal State Error"
    wlan.active(False)
    time.sleep(0.2)
    wlan.active(True)
    
    print("\n--- CONFIGURACIÓN DE RED AUTOMÁTICA ---")
    ssid = "Mkl bilder"
    password = ""  # TODO: add password
    
    print(f"\nConectando a la red: {ssid}...")
    wlan.connect(ssid, password)
    
    timeout = 15
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
        print("⚡", end="")
        
    if wlan.isconnected():
        # Corregido usando estrictamente el índice [0] para la IP dinámica
        print(f"\n\n[OK] ¡Conectado con éxito a {ssid}!")
        print(f"[WIFI] Dirección IP asignada: {wlan.ifconfig()[0]}")
        print("-" * 40)
        return True
    else:
        print("\n\n[ERROR] No se pudo conectar. Verifica los datos.")
        print("-" * 40)
        return False

# --- FLUJO PRINCIPAL DE ARRANQUE ---
# Ejecutamos el menú con contador antes de levantar el WiFi o el main
if menu_inicio(timeout_segundos=5):
    conectar_wifi_interactivo()
else:
    # Si eliges la opción 2, cerramos el script para darte el control total de Thonny
    sys.exit()