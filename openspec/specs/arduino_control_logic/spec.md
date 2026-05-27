# Arduino Control Logic

## Purpose
This specification defines the firmware behavior of the Arduino Nano, including actuator driving, sensor reading, and input mixing.

## Requirements

### Requirement: Pin Assignment and Hardware Interfaces
The Arduino Nano MUST map its input/output pins to the respective joysticks and motor drivers.
- **Joysticks (ADC Inputs)**:
  - Carro (X) -> A0
  - Elevación (Y) -> A1
  - Giro (Z) -> A2
- **Driver TB6612FNG (Motores DC)**:
  - Motor A (Carro): AIN1 = D2, AIN2 = D4, PWMA = D3
  - Motor B (Elevación): BIN1 = D7, BIN2 = D8, PWMB = D5
- **Driver DRV8825 (Stepper)**:
  - STEP = D9
  - DIR = D10

#### Scenario: Driver Initialization
- **WHEN** the setup function is called on boot
- **THEN** all control and driver pins must be configured to the correct PinMode and initial state.

### Requirement: Joystick Zone Dead Band and Mapping
The local analog joystick inputs MUST be mapped to the motor speeds with a dead zone.
- Dead band: Between values 480 and 540 (to avoid drift when centered).
- Scale: Map 0-480 to negative speed (-maxVal to 0) and 540-1023 to positive speed (0 to maxVal).

#### Scenario: Joystick in Dead Band
- **WHEN** the analog reading is between 481 and 539
- **THEN** the returned control intent speed must be 0.

### Requirement: Dual-Input Movement Mixing
The control loops SHALL combine physical joystick inputs and serial command inputs to calculate final motor output speeds.
- Combined Speed = Joystick Intent + Remote Web Intent
- Motor speeds must be constrained to the range [-255, 255] for DC motors.
- Stepper speed must be constrained to the range [-MAX_STEPPER_SPEED, MAX_STEPPER_SPEED].

#### Scenario: Dual Controls Concurrent Action
- **WHEN** a joystick input is mapped to speed 100 and a remote UART command sets intent speed to 255
- **THEN** the combined target speed must be constrained to 255.
