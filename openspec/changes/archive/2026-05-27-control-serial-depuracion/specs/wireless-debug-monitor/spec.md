## ADDED Requirements

### Requirement: SoftwareSerial Log Output on Arduino
The Arduino Nano MUST transmit text logs to a secondary emulated serial port.
- SoftwareSerial Config: RX on pin D13 (unused), TX on pin D12 at 9600 bps.
- Output: Redirection of all events, commands, and warning logs to this port.

#### Scenario: Arduino Emits Log
- **WHEN** a motor status changes or a local button is debounced
- **THEN** Arduino writes the log text string over debugSerial followed by a newline.

### Requirement: ESP32 Wireless Log Server
The ESP32 firmware MUST read secondary serial logs, store them in a ring buffer, and serve them over socket connections on port 80.
- Buffer: Ring buffer in RAM storing the last 50 lines.
- Port: HTTP Port 80.
- Endpoint `/` : Serves an HTML page with retro green terminal style.
- Page header: `<meta http-equiv="refresh" content="2">` for auto-refresco.

#### Scenario: Serve Remote Log Monitor
- **WHEN** a client accesses http://<esp32-ip>/
- **THEN** the ESP32 serves the retro HTML page rendering the last 50 lines of logs from the ring buffer.
