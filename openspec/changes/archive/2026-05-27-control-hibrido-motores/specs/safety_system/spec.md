## MODIFIED Requirements

### Requirement: Arduino UART Connection Watchdog
The Arduino Nano control firmware MUST run a safety timer to detect loss of control command link when in Web mode.
- Watchdog Timeout: 500 milliseconds.
- Trigger: Lack of incoming valid UART movement command (`F`, `B`, `U`, `D`, `L`, `R`, `S`) while in Web mode.
- Action: Reset the web-sourced movement intent variables to zero.

#### Scenario: Loss of Communication Link
- **WHEN** the time since the last valid UART command exceeds 500 ms and `modoControlWeb` is True
- **THEN** the local web intent registers for carriage, hoisting, and rotation must be set to 0.

### Requirement: Emergency Stop Handling
The system SHALL treat the command character `S` as an immediate stop signal for all three DC motor actuators.
- Action: Disable H-Bridge driver outputs (PWMA=0, PWMB=0, PWMC=0).

#### Scenario: Emergency Stop Command Received
- **WHEN** an ASCII `S` is received via UART or the emergency button is pressed
- **THEN** the motor driver PWM pins must go to zero.
