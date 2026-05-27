# electronic-schematic Specification

## Purpose
TBD - created by archiving change control-hibrido-motores. Update Purpose after archive.
## Requirements
### Requirement: Electronic Connections Diagram
The project MUST include a web-viewable diagram file named Schema.html under the web_server folder that details all pin connections.
- Path: `/web_server/Schema.html`
- Visual updates: Detail the SoftwareSerial connection between Arduino Nano D12 (TX) and ESP32 RX (GPIO 16).
- Navigation: Add a clear navigation link in the header to return to `/web_server/index.html`.

#### Scenario: Visual Verification of Connections
- **WHEN** the user opens `/web_server/Schema.html` in a web browser
- **THEN** it must clearly render the new SoftwareSerial log link and provide a navigation link back to index.html.

