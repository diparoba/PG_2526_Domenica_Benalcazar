# OpenSpec: Sistema de Control de Grúa Torre (v2)

## 1. Protocolo de Comunicación (UART)
Configuración física: 9600 baudios, 8N1. Unidireccional (ESP32 TX GPIO 17 -> Arduino RX D0).

**Mapeo de Comandos:**
- `F`/`B`: Traslación Carro | `U`/`D`: Elevación | `L`/`R`: Giro Pluma | `S`: Parada de Emergencia.

## 2. API Web (Endpoint)
El servidor ESP32 expone: `GET /api/command?cmd={char}`.
- Respuesta: `200 OK` (Texto plano: `OK`).

## 3. Lógica de Control (Firmware Arduino)
- **Actuadores:** Motores DC (TB6612FNG) y Motor Paso a Paso Nema 17 (DRV8825).
- **Seguridad:** El estado de reposo `'S'` se activa automáticamente si no se reciben tramas válidas durante un periodo superior a 600ms.