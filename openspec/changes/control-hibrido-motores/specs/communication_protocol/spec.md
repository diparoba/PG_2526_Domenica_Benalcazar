## MODIFIED Requirements

### Requirement: Control Commands
The system SHALL support simple, single-character ASCII commands for actions and modes:
- `F` = Move trolley forward
- `B` = Move trolley backward
- `U` = Raise hook
- `D` = Lower hook
- `L` = Rotate jib left
- `R` = Rotate jib right
- `S` = Emergency Stop / Standby
- `W` = Activate Web Control Mode
- `M` = Activate Manual (Joystick) Control Mode

#### Scenario: Processing Valid Command
- **WHEN** the Arduino Nano receives a valid command character over serial
- **THEN** it updates the corresponding target movement intent or control mode state.

#### Scenario: Mode Synchronization Command
- **WHEN** the Arduino Nano changes control mode via physical button press
- **THEN** it must transmit the new mode character ('W' or 'M') over UART to the ESP32.
