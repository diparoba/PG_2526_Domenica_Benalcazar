# UART Communication Protocol

## Purpose
This specification defines the serial communication protocol between the ESP32 (Web Gateway) and the Arduino Nano (Motor Actuator).

## Requirements

### Requirement: UART Configuration
The serial connection MUST use a standard baud rate of 9600 bps and 8N1 format.
- **Baud Rate**: 9600 bps
- **Data Bits**: 8
- **Parity**: None
- **Stop Bits**: 1
- **Physical Pins**: ESP32 TX (GPIO 17) -> Arduino RX

#### Scenario: Normal UART Initialization
- **WHEN** the system boots up
- **THEN** the serial ports on both microcontrollers must be initialized to 9600 8N1.

### Requirement: Control Commands
The system SHALL support simple, single-character ASCII commands for actions.
- `F` = Move trolley forward
- `B` = Move trolley backward
- `U` = Raise hook
- `D` = Lower hook
- `L` = Rotate jib left
- `R` = Rotate jib right
- `S` = Emergency Stop / Standby

#### Scenario: Processing Valid Command
- **WHEN** the Arduino Nano receives a valid command character over serial
- **THEN** it updates the corresponding target movement intent.
