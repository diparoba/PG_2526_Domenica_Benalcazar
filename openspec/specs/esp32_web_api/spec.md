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
The ESP32 HTTP Server SHALL NOT handle command, status, or telemetry API routes, but instead serve only the terminal log viewer at root.
- `/` : Serve the lightweight logs page with retro green terminal aesthetics and auto-refresh header.
- All other API routes (`/api/command`, `/api/status`, `/api/mode`, `/api/logs`) MUST be removed.

#### Scenario: Serve Log Interface
- **WHEN** the user visits the root IP address on port 80
- **THEN** the ESP32 serves the simple HTML page containing the log list.

