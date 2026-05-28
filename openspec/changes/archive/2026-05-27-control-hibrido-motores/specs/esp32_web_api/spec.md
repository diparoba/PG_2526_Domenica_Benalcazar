## MODIFIED Requirements

### Requirement: Web HTTP API Endpoints
The HTTP Server SHALL handle incoming requests and route them to API endpoints.
- `/` : Serve local `index.html` interface.
- `/api/command?cmd={F|B|U|D|L|R|S}` : Parse command parameter, trigger serial write, and return a JSON status.
- `/api/telemetry` or `/api/logs` : Serve raw event logging and telemetry data.
- `/api/status` : Return current mode status `{"mode": "web" | "manual"}`.
- `/api/mode?set={web|manual}` : Toggle control mode and notify Arduino Nano.

#### Scenario: Received Command Endpoint Request
- **WHEN** a client calls `GET /api/command?cmd=F`
- **THEN** the server must parse the command, send it over UART, and reply with HTTP 200 and a JSON status.

#### Scenario: Set Mode Request
- **WHEN** a client calls `GET /api/mode?set=manual`
- **THEN** the server must set its local state to manual, send character 'M' over UART, and return JSON status.

### Requirement: Input Priority Resolution
The ESP32 control loop MUST resolve control input conflict and synchronize mode changes with the Arduino Nano.
- The ESP32 must read UART data. If it receives 'W' or 'M' from the Arduino, it must update its local `modo_control_web` state.
- High Priority: If `modo_control_web` is True, it must send commands from the Web interface or physical backup buttons to the Arduino.
- Low Priority: If `modo_control_web` is False, the ESP32 does not send movement commands to Arduino (letting the Arduino run in manual mode using its local joysticks).

#### Scenario: Standby Command From Web
- **WHEN** the web control command is 'S' and `modo_control_web` is True
- **THEN** the ESP32 control loop must check and transmit commands from physical backup inputs.
