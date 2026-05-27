# Sistema de Control Híbrido para Grúa Torre (ESP32 + Arduino Nano)

Este proyecto desarrolla una solución mecatrónica para el control automatizado de una grúa torre a escala, integrando una arquitectura de doble procesador para la gestión de actuadores y una interfaz de usuario remota vía red inalámbrica.

## 1. Requisitos del Proyecto
- **Control de Actuadores:** Gestión de dos motores DC (N20) y un motor paso a paso (Nema 17) mediante drivers TB6612FNG y DRV8825.
- **Control Dual:** Implementación de lógica de prioridad que permite alternar entre mandos manuales locales (joysticks) y remotos (web).
- **Arquitectura de Procesamiento:** - **ESP32 DevKit V1:** Servidor web asíncrono en MicroPython.
    - **Arduino Nano:** Ejecución de control de potencia y cinemática en tiempo real.
- **Seguridad:** Protocolo de "hombre muerto" mediante *watchdog* por software, forzando estado de reposo ('S') ante pérdida de enlace.
- **Comunicación:** Enlace UART asíncrono (9600 bps) entre procesadores.

## 2. Task Log (Estado de Implementación)
La siguiente tabla resume el progreso y la validación de las tareas críticas del sistema:

| Tarea | Descripción | Estado |
| :--- | :--- | :--- |
| **Tarea 1** | Firmware Arduino (Control, PWM, Step, UART) | [x] |
| **Tarea 2** | Firmware ESP32 (uasyncio, Server, UART) | [x] |
| **Tarea 3** | Interfaz Web (Diseño, Fetch API, Táctil) | [x] |
| **Tarea 4** | Documentación Técnica (OpenSpec) | [x] |
| **Tarea 5** | Planos y Diseño de Hardware | [x] |
| **Tarea 6** | Integración y Pruebas de Seguridad | [ ] |

## 3. Guía de Operación
1. **Red:** El sistema genera el AP `Grua_Torre_Politecnica`.
2. **Interfaz:** Acceder a `192.168.4.1` desde un navegador móvil.
3. **Prioridad:** Los comandos vía web anulan los joysticks físicos hasta que el estado web retorne a 'S'.