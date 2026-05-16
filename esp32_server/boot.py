import network
import time

SSID = "WIFI_GRUA"
PASSWORD = "password123"

def connect_wifi():
    print("Iniciando configuracion WiFi...")
    # Configurar como Station (conectarse a un router)
    # Si deseas que la grúa cree su propia red, cambia a network.AP_IF
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"Conectando a {SSID}...")
        wlan.connect(SSID, PASSWORD)
        
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

connect_wifi()
