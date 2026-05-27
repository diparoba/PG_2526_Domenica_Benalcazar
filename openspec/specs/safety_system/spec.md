# Safety Watchdog and Emergency Stop System

## Purpose
This specification defines the safety systems of the grúa torre scale model, including the connection watchdog timer and emergency stop behaviors.

## Requirements

### Requirement: Arduino UART Connection Watchdog
The Arduino Nano control firmware MUST run a safety timer to detect loss of control command link.
- Watchdog Timeout: 500 milliseconds.
- Trigger: Lack of incoming valid UART movement command (`F`, `B`, `U`, `D`, `L`, `R`, `S`).
- Action: Reset the web-sourced movement intent variables to zero.

#### Scenario: Loss of Communication Link
- **WHEN** the time since the last valid UART command exceeds 500 ms
- **THEN** the local web intent registers for carriage, hoisting, and rotation must be set to 0.

### Requirement: Emergency Stop Handling
The system SHALL treat the command character `S` as an immediate stop signal for all actuators.
- Action: Disable H-Bridge driver outputs (PWMA=0, PWMB=0) and stop the Stepper driver stepping signal.

#### Scenario: Emergency Stop Command Received
- **WHEN** an ASCII `S` is received via UART or the emergency button is pressed
- **THEN** the motor driver PWM pins must go to zero and stepper speed must be set to zero.
