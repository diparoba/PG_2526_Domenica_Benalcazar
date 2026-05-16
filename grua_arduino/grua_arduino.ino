#include <AccelStepper.h>

// Definición de pines - Joysticks
#define JOY_X_PIN A0    // Carro
#define JOY_Y_PIN A1    // Elevación
#define JOY_Z_PIN A2    // Giro

// Definición de pines - Motor A (Carro) TB6612FNG
#define AIN1_PIN 2
#define AIN2_PIN 4
#define PWMA_PIN 3

// Definición de pines - Motor B (Elevación) TB6612FNG
#define BIN1_PIN 7
#define BIN2_PIN 8
#define PWMB_PIN 5

// Definición de pines - Motor a Pasos (Giro) DRV8825
#define STEP_PIN 9
#define DIR_PIN 10

// Parámetros del motor a pasos
#define MAX_STEPPER_SPEED 1000.0
#define STEPPER_ACCEL 500.0

// Instancia de AccelStepper
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

// Variables de intención web
int webCarro = 0;
int webElevacion = 0;
float webGiro = 0.0;
unsigned long lastWebCmdTime = 0;
const unsigned long WEB_TIMEOUT_MS = 500; // Timeout de 500ms para seguridad

void setup() {
  // Inicialización de comunicación serial
  Serial.begin(9600);

  // Configuración de pines de motores DC
  pinMode(AIN1_PIN, OUTPUT);
  pinMode(AIN2_PIN, OUTPUT);
  pinMode(PWMA_PIN, OUTPUT);
  
  pinMode(BIN1_PIN, OUTPUT);
  pinMode(BIN2_PIN, OUTPUT);
  pinMode(PWMB_PIN, OUTPUT);

  // Configuración inicial de AccelStepper
  stepper.setMaxSpeed(MAX_STEPPER_SPEED);
  stepper.setAcceleration(STEPPER_ACCEL);
}

// Función auxiliar para leer y mapear el joystick con zona muerta
int readJoystick(int pin, int maxVal) {
  int val = analogRead(pin);
  // Zona muerta entre 480 y 540
  if (val > 480 && val < 540) {
    return 0;
  }
  // Mapear de 0-480 y 540-1023 a -maxVal a maxVal
  if (val <= 480) {
    return map(val, 0, 480, -maxVal, 0);
  } else {
    return map(val, 540, 1023, 0, maxVal);
  }
}

// Función para controlar el Motor A (Carro)
void controlMotorA(int speed) {
  speed = constrain(speed, -255, 255);
  if (speed == 0) {
    digitalWrite(AIN1_PIN, LOW);
    digitalWrite(AIN2_PIN, LOW);
    analogWrite(PWMA_PIN, 0);
  } else if (speed > 0) {
    digitalWrite(AIN1_PIN, HIGH);
    digitalWrite(AIN2_PIN, LOW);
    analogWrite(PWMA_PIN, speed);
  } else {
    digitalWrite(AIN1_PIN, LOW);
    digitalWrite(AIN2_PIN, HIGH);
    analogWrite(PWMA_PIN, -speed);
  }
}

// Función para controlar el Motor B (Elevación)
void controlMotorB(int speed) {
  speed = constrain(speed, -255, 255);
  if (speed == 0) {
    digitalWrite(BIN1_PIN, LOW);
    digitalWrite(BIN2_PIN, LOW);
    analogWrite(PWMB_PIN, 0);
  } else if (speed > 0) {
    digitalWrite(BIN1_PIN, HIGH);
    digitalWrite(BIN2_PIN, LOW);
    analogWrite(PWMB_PIN, speed);
  } else {
    digitalWrite(BIN1_PIN, LOW);
    digitalWrite(BIN2_PIN, HIGH);
    analogWrite(PWMB_PIN, -speed);
  }
}

void processUART() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    
    // Si recibimos un comando válido, actualizamos el tiempo del último comando
    if (cmd == 'F' || cmd == 'B' || cmd == 'U' || cmd == 'D' || cmd == 'L' || cmd == 'R' || cmd == 'S') {
      lastWebCmdTime = millis();
    }
    
    // Limpiamos intenciones si es comando de movimiento, para no mezclar direcciones contradictorias de la web
    switch (cmd) {
      case 'F': webCarro = 255; break;
      case 'B': webCarro = -255; break;
      case 'U': webElevacion = 255; break;
      case 'D': webElevacion = -255; break;
      case 'L': webGiro = -MAX_STEPPER_SPEED; break;
      case 'R': webGiro = MAX_STEPPER_SPEED; break;
      case 'S': 
        webCarro = 0; 
        webElevacion = 0; 
        webGiro = 0.0; 
        break;
    }
  }

  // Timeout de seguridad web
  if (millis() - lastWebCmdTime > WEB_TIMEOUT_MS) {
    webCarro = 0;
    webElevacion = 0;
    webGiro = 0.0;
  }
}

void loop() {
  // Procesar comandos de la interfaz web
  processUART();

  // Leer intenciones del joystick
  int joyCarro = readJoystick(JOY_X_PIN, 255);
  int joyElevacion = readJoystick(JOY_Y_PIN, 255);
  int joyGiro = readJoystick(JOY_Z_PIN, MAX_STEPPER_SPEED);

  // Lógica mixta: Suma de intención joystick + intención web
  int velCarroFinal = joyCarro + webCarro;
  int velElevacionFinal = joyElevacion + webElevacion;
  float velGiroFinal = (float)joyGiro + webGiro;

  // Ejecutar movimientos
  controlMotorA(velCarroFinal);
  controlMotorB(velElevacionFinal);

  // Control del Stepper (Giro)
  velGiroFinal = constrain(velGiroFinal, -MAX_STEPPER_SPEED, MAX_STEPPER_SPEED);
  if (abs(velGiroFinal) > 0) {
    stepper.setSpeed(velGiroFinal);
    stepper.runSpeed();
  } else {
    stepper.setSpeed(0);
    stepper.stop();
  }
}
