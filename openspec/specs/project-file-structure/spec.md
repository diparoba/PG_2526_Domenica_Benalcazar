# project-file-structure Specification

## Purpose
TBD - created by archiving change control-serial-depuracion. Update Purpose after archive.
## Requirements
### Requirement: Repository Clean Organization
The repository files MUST be organized into dedicated folders by subsystem.
- Folder `/arduino/` : Holds the Arduino Nano source code file grua_arduino.ino.
- Folder `/esp32/` : Holds the ESP32 MicroPython files boot.py and main.py.
- Folder `/web_server/` : Holds the laptop-hosted files index.html and Schema.html.

#### Scenario: File Cleanliness Verification
- **WHEN** the files are sorted into /arduino/, /esp32/, and /web_server/
- **THEN** all equivalent copies or duplicate files must be deleted from the root directory.

