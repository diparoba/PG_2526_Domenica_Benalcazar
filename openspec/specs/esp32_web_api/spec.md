# ESP32 Web Gateway and API

## Purpose
This specification defines the behavior of the ESP32 server, including WiFi connectivity, the HTTP API endpoints, event logging, and the hybrid priority control loop.

## Requirements

### Requirement: Boot Menu and WiFi Connectivity
The ESP32 firmware MUST present an interactive boot menu with a timeout and configure WiFi connectivity.
- Option 1 (Execution Mode): Automatically connects using interactive input or dynamic IP configuration.
- Option 2 (Programming Mode): Stops startup script execution and releases the REPL interface.

#### Scenario: Auto Start Timeout
- **WHEN** the system boots up and no input is received within 5 seconds
- **THEN** it must proceed to configuration and startup.

### Requirement: Web HTTP API Endpoints
The HTTP Server SHALL handle incoming requests and route them to API endpoints.
- `/` : Serve local `index.html` interface.
- `/api/command?cmd={F|B|U|D|L|R|S}` : Parse command parameter, trigger serial write, and return a JSON status.
- `/api/telemetry` or `/api/logs` : Serve raw event logging and telemetry data.

#### Scenario: Received Command Endpoint Request
- **WHEN** a client calls `GET /api/command?cmd=F`
- **THEN** the server must parse the command, send it over UART, and reply with HTTP 200 and a JSON status.

### Requirement: Input Priority Resolution
The ESP32 control loop MUST resolve control input conflict by assigning priorities.
- High Priority: If a web control command is active (not 'S'), it must override physical inputs.
- Low Priority: If the web control command is 'S' (standby/stop), the loop must evaluate physical inputs (e.g. backup buttons/joysticks).

#### Scenario: Standby Command From Web
- **WHEN** the web control command is 'S'
- **THEN** the ESP32 control loop must check and transmit commands from physical backup inputs.
