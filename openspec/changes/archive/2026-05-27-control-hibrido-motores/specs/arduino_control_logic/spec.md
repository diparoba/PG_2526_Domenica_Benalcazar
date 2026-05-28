## MODIFIED Requirements

### Requirement: Pin Assignment and Hardware Interfaces
The Arduino Nano MUST map its input/output pins to the respective joysticks and H-bridge motor drivers.
- **Joysticks (ADC Inputs)**:
  - Carro (X) -> A0
  - Elevación (Y) -> A1
  - Giro (Z) -> A2
- **Driver TB6612FNG 1 (Motores DC)**:
  - Motor A (Carro): AIN1 = D2, AIN2 = D4, PWMA = D3
  - Motor B (Elevación): BIN1 = D7, BIN2 = D8, PWMB = D5
- **Driver TB6612FNG 2 (Motor DC - NUEVO)**:
  - Motor C (Giro): CIN1 = D9, CIN2 = D10, PWMC = D6
- **Physical Mode Button**:
  - Joystick button -> D11 (with internal pull-up)

#### Scenario: Driver Initialization
- **WHEN** the setup function is called on boot
- **THEN** all control and driver pins must be configured to the correct PinMode and initial state, including disabling AccelStepper and initializing the D6 pin for PWM.

### Requirement: Joystick Zone Dead Band and Mapping
The local analog joystick inputs MUST be mapped to the motor speeds with a dead zone and respect maximum speed configurations.
- Dead band: Between values 480 and 540 (to avoid drift when centered).
- Scale: Map 0-480 to negative maximum speed and 540-1023 to positive maximum speed.
- Max speeds MUST be configurable via constant variables (`MAX_VEL_CARRO`, `MAX_VEL_ELEVACION`, `MAX_VEL_GIRO`).

#### Scenario: Joystick in Dead Band
- **WHEN** the analog reading is between 481 and 539
- **THEN** the returned control intent speed must be 0.

#### Scenario: Joystick Full Deflection
- **WHEN** the joystick is deflected fully to the positive direction
- **THEN** the output speed must match the configured maximum speed for that channel.

### Requirement: Dual-Input Movement Mixing
The control loops SHALL NOT combine physical joystick inputs and serial command inputs, but instead execute them exclusively based on the active mode.
- If `modoControlWeb` is True: the Arduino Nano executes remote commands and ignores joystick inputs.
- If `modoControlWeb` is False: the Arduino Nano executes local joystick inputs and ignores remote commands.

#### Scenario: Dual Controls Concurrent Action
- **WHEN** the system is in manual mode (`modoControlWeb` is False) and web commands are received
- **THEN** the system must ignore web commands and only execute joystick inputs.

## ADDED Requirements

### Requirement: Physical Mode Toggle Button
The Arduino Nano MUST monitor pin `D11` for a press action of the physical joystick button to toggle modes.
- Input configuration: Internal Pull-Up enabled.
- Debounce: Implement a software debounce of at least 50 ms.
- Action: Toggle the value of `modoControlWeb` and transmit the state (`W` or `M`) via UART.

#### Scenario: Button Press Toggle
- **WHEN** the physical joystick button is pressed and held for 60 ms
- **THEN** the control mode must toggle and send a serial status byte to the ESP32.
