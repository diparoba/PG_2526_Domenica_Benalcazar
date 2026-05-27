## ADDED Requirements

### Requirement: Direct Web Serial Connection
The Web interface MUST implement direct, Chrome/Edge native serial communication with the Arduino Nano via USB.
- Connection action: A "Conectar USB" button in the interface.
- Baud Rate: 9600 bps.
- Mode: Direct reading and writing without page reload.

#### Scenario: User connects USB
- **WHEN** the user clicks "Conectar USB" and selects the Arduino COM port
- **THEN** the browser opens the serial port and enables control key listeners.

### Requirement: Telemetry JSON Parsing
The Web interface JS code SHALL read incoming serial data stream, assemble it into lines, parse it as JSON, and update the UI monitors.
- Format: `{"giro": angle, "carro": position, "gancho": depth}`.
- Update frequency: Updates the digital twin SVG and charts instantly upon receiving a valid JSON line.

#### Scenario: Parsing Valid Telemetry Frame
- **WHEN** the serial port receives `{"giro": 45, "carro": 120, "gancho": 10}`
- **THEN** the interface must update the planta angle to 45, carro position to 120, and gancho depth to 10.
