## MODIFIED Requirements

### Requirement: Pin Assignment and Hardware Interfaces
The Arduino Nano MUST map its input/output pins to the respective joysticks, H-bridge motor drivers, and the secondary log software serial.
- **Joysticks (ADC Inputs)**:
  - Carro (X) -> A0
  - Elevación (Y) -> A1
  - Giro (Z) -> A2
- **Driver TB6612FNG 1 (Motores DC)**:
  - Motor A (Carro): AIN1 = D2, AIN2 = D4, PWMA = D3
  - Motor B (Elevación): BIN1 = D7, BIN2 = D8, PWMB = D5
- **Driver TB6612FNG 2 (Motor DC)**:
  - Motor C (Giro): CIN1 = D9, CIN2 = D10, PWMC = D6
- **Physical Mode Button**:
  - Joystick button -> D11 (with internal pull-up)
- **SoftwareSerial Interface (Logs)**:
  - debugSerial RX -> D13 (unused)
  - debugSerial TX -> D12 (connected to ESP32 RX)

#### Scenario: Driver Initialization
- **WHEN** the setup function is called on boot
- **THEN** all control, driver, and software serial pins must be configured to the correct PinMode and initial state.

### Requirement: Dual-Input Movement Mixing
The control loops SHALL NOT combine physical joystick inputs and serial command inputs, but instead execute them exclusively based on the active mode.
- If `modoControlWeb` is True: the Arduino Nano executes remote USB serial commands and ignores joystick inputs.
- If `modoControlWeb` is False: the Arduino Nano executes local joystick inputs and ignores USB serial commands.
- Telemetry: The Arduino Nano must periodically output JSON string status `{"giro": angle, "carro": position, "gancho": depth}` on the hardware serial USB port for the laptop browser.

#### Scenario: Dual Controls Concurrent Action
- **WHEN** the system is in manual mode (`modoControlWeb` is False) and web USB commands are received
- **THEN** the system must ignore web commands and only execute joystick inputs.
