# ==========================================================
# ARCHIVO: boot.py
# DESCRIPCIÓN: Conexión inicial a la red WiFi (Sin bloqueos)
# ==========================================================
import network
import time

def conectar_wifi_universal():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Si la placa ya se conectó sola al arrancar
    if wlan.isconnected():
        print(f"\n[WIFI] Conexión automática activa: {wlan.config('ssid')}")
        print(f"[WIFI] Dirección IP: {wlan.ifconfig()[0]}")
        return True
        
    print("\n--- CONFIGURACIÓN DE RED GRÚA TORRE ---")
    ssid_predeterminado = "Cudy-0138" # Red de tu aula/colegio
    
    print(f"Buscando red predeterminada: {ssid_predeterminado}...")
    wlan.connect(ssid_predeterminado)
    
    # Esperar un momento a la conexión automática
    timeout = 8
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
        print("⚡", end="")
        
    if wlan.isconnected():
        print(f"\n[OK] ¡Conectado con éxito a {wlan.config('ssid')}!")
        print(f"[WIFI] Dirección IP: {wlan.ifconfig()[0]}")
        return True
    
    # Si falla, pide ingresar los datos manualmente por consola
    print("\n[AVISO] No se detectó la red automática.")
    ssid = input("Ingresa el nombre de tu WiFi (SSID): ").strip()
    password = input("Ingresa la contraseña del WiFi: ").strip()
    
    print(f"Conectando a {ssid}...")
    wlan.connect(ssid, password)
    
    timeout = 12
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
        print("⚡", end="")
        
    if wlan.isconnected():
        print(f"\n[OK] ¡Conectado con éxito a {ssid}!")
        print(f"[WIFI] Dirección IP: {wlan.ifconfig()[0]}")
        return True
    else:
        print("\n[ERROR] No se pudo conectar al WiFi.")
        return False

# Arrancar la conexión
conectar_wifi_universal()