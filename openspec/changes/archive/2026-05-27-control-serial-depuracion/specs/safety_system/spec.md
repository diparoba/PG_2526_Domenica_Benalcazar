## MODIFIED Requirements

### Requirement: Arduino UART Connection Watchdog
The Arduino Nano control firmware MUST run a safety timer to detect loss of control command link over USB Web Serial when in Web mode.
- Watchdog Timeout: 500 milliseconds.
- Trigger: Lack of incoming valid Web Serial USB movement command (`F`, `B`, `U`, `D`, `L`, `R`, `S`) while in Web mode.
- Action: Reset the web-sourced movement intent variables to zero.

#### Scenario: Loss of Communication Link
- **WHEN** the time since the last valid Web Serial command exceeds 500 ms and `modoControlWeb` is True
- **THEN** the local web intent registers for carriage, hoisting, and rotation must be set to 0.
