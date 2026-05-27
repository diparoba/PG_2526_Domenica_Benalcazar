## ADDED Requirements

### Requirement: Electronic Connections Diagram
The project MUST include a web-viewable diagram file named `Schema.html` that details all pin connections between components.
- Path: `Schema.html` in the project root.
- Formatting: Uses standard HTML/CSS/SVG.
- Visual elements: Color-coded lines and interactive pins to trace connections easily.

#### Scenario: Visual Verification of Connections
- **WHEN** the user opens `Schema.html` in a web browser
- **THEN** it must clearly render the connections between Arduino Nano, ESP32, the two TB6612FNG drivers, and input joysticks.
