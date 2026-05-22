# Sistema de Control Híbrido para Grúa Torre (ESP32 + Arduino Nano)

Este proyecto desarrolla una solución de control para una grúa torre industrial a escala, integrando una arquitectura de doble procesador para la gestión de actuadores y la interfaz de usuario remota.

## Arquitectura del Sistema
- **Unidad de Servidor (ESP32 DevKit V1):** Gestiona la infraestructura de red mediante un servidor web asíncrono (`uasyncio`), operando bajo un Punto de Acceso (AP) dedicado.
- **Unidad de Control (Arduino Nano):** Gestiona la cinemática de los actuadores (motores DC y motor paso a paso) mediante el parseo de comandos seriales (UART).

## Características Técnicas
- **Control Dual:** Sistema de operación concurrente que permite la entrada de comandos remotos (vía web) y manuales (vía joysticks físicos).
- **Seguridad Industrial:** Implementación de un mecanismo de *watchdog* (timeout de seguridad) que garantiza la detención inmediata de los actuadores ante la pérdida del enlace inalámbrico.
- **Eficiencia:** Comunicación serial de baja latencia a 9600 bps y procesamiento no bloqueante en ambos microcontroladores.