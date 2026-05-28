## MODIFIED Requirements

### Requirement: Web HTTP API Endpoints
The ESP32 HTTP Server SHALL NOT handle command, status, or telemetry API routes, but instead serve only the terminal log viewer at root.
- `/` : Serve the lightweight logs page with retro green terminal aesthetics and auto-refresh header.
- All other API routes (`/api/command`, `/api/status`, `/api/mode`, `/api/logs`) MUST be removed.

#### Scenario: Serve Log Interface
- **WHEN** the user visits the root IP address on port 80
- **THEN** the ESP32 serves the simple HTML page containing the log list.

## REMOVED Requirements

### Requirement: Input Priority Resolution
**Reason**: Control commands have been completely offloaded from the ESP32. The laptop browser communicates directly with the Arduino Nano via Web Serial USB.
**Migration**: All control inputs, modes, and mixing priorities are resolved locally on the Arduino Nano or laptop browser JS.
