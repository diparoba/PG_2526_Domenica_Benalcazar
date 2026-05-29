#include <SoftwareSerial.h>

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

// Definición de pines - Motor C (Giro) TB6612FNG (Canal A/B del segundo puente H)
#define CIN1_PIN 9
#define CIN2_PIN 10
#define PWMC_PIN 6

// Botón de Modo
#define JOY_BTN_PIN 11

// SoftwareSerial para logs de depuración hacia ESP32
SoftwareSerial debugSerial(13, 12); // RX = 13 (sin usar), TX = 12 (conectado a ESP32 G16)

// Parámetros de velocidad máxima configurable
#define MAX_VEL_CARRO 200
#define MAX_VEL_ELEVACION 200
#define MAX_VEL_GIRO 200

// Variables de intención web
int webCarro = 0;
int webElevacion = 0;
int webGiro = 0;
unsigned long lastWebCmdTime = 0;
const unsigned long WEB_TIMEOUT_MS = 500; // Timeout de 500ms para seguridad

// Estado del modo de control (false = Manual/Joystick, true = Web)
bool modoControlWeb = false;
unsigned long lastBtnPressTime = 0;
const unsigned long DEBOUNCE_MS = 50;
bool lastBtnState = HIGH;

// Variables del gemelo digital de telemetría (Simuladas en Arduino)
float posGiro = 0.0;
float posCarro = 110.0;
float posGancho = 0.0;

unsigned long lastUpdate = 0;
unsigned long lastTelemetryTime = 0;
const unsigned long TELEMETRY_INTERVAL_MS = 100; // Telemetría cada 100ms

void setup() {
  // Inicialización de comunicación serial de hardware (USB-Laptop)
  Serial.begin(9600);

  // Inicialización de SoftwareSerial para depuración (hacia ESP32)
  debugSerial.begin(9600);
  debugSerial.println("SYSTEM: Crane controller initialized. Logs redirected here.");

  // Configuración de pines de motores DC
  pinMode(AIN1_PIN, OUTPUT);
  pinMode(AIN2_PIN, OUTPUT);
  pinMode(PWMA_PIN, OUTPUT);
  
  pinMode(BIN1_PIN, OUTPUT);
  pinMode(BIN2_PIN, OUTPUT);
  pinMode(PWMB_PIN, OUTPUT);

  pinMode(CIN1_PIN, OUTPUT);
  pinMode(CIN2_PIN, OUTPUT);
  pinMode(PWMC_PIN, OUTPUT);

  // Configuración de botón físico
  pinMode(JOY_BTN_PIN, INPUT_PULLUP);
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
  speed = constrain(speed, -MAX_VEL_CARRO, MAX_VEL_CARRO);
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
  speed = constrain(speed, -MAX_VEL_ELEVACION, MAX_VEL_ELEVACION);
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

// Función para controlar el Motor C (Giro)
void controlMotorC(int speed) {
  speed = constrain(speed, -MAX_VEL_GIRO, MAX_VEL_GIRO);
  if (speed == 0) {
    digitalWrite(CIN1_PIN, LOW);
    digitalWrite(CIN2_PIN, LOW);
    analogWrite(PWMC_PIN, 0);
  } else if (speed > 0) {
    digitalWrite(CIN1_PIN, HIGH);
    digitalWrite(CIN2_PIN, LOW);
    analogWrite(PWMC_PIN, speed);
  } else {
    digitalWrite(CIN1_PIN, LOW);
    digitalWrite(CIN2_PIN, HIGH);
    analogWrite(PWMC_PIN, -speed);
  }
}

void processUART() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    
    // Si recibimos un comando de movimiento válido, actualizamos el tiempo del último comando
    if (cmd == 'F' || cmd == 'B' || cmd == 'U' || cmd == 'D' || cmd == 'L' || cmd == 'R' || cmd == 'S') {
      lastWebCmdTime = millis();
      debugSerial.print("UART: Movement command received: ");
      debugSerial.println(cmd);
    }
    
    switch (cmd) {
      case 'F': webCarro = MAX_VEL_CARRO; break;
      case 'B': webCarro = -MAX_VEL_CARRO; break;
      case 'U': webElevacion = MAX_VEL_ELEVACION; break;
      case 'D': webElevacion = -MAX_VEL_ELEVACION; break;
      case 'L': webGiro = -MAX_VEL_GIRO; break;
      case 'R': webGiro = MAX_VEL_GIRO; break;
      case 'S': 
        webCarro = 0; 
        webElevacion = 0; 
        webGiro = 0; 
        debugSerial.println("ACTION: Emergency Stop / Standby.");
        break;
      case 'W':
        if (!modoControlWeb) {
          modoControlWeb = true;
          Serial.write('W');
          debugSerial.println("MODE: Changed to WEB (Remote control active).");
        }
        break;
      case 'M':
        if (modoControlWeb) {
          modoControlWeb = false;
          Serial.write('M');
          debugSerial.println("MODE: Changed to MANUAL (Joystick control active).");
        }
        break;
    }
  }

  // Timeout de seguridad web: solo se aplica si está en modo Web
  if (modoControlWeb && (millis() - lastWebCmdTime > WEB_TIMEOUT_MS)) {
    if (webCarro != 0 || webElevacion != 0 || webGiro != 0) {
      webCarro = 0;
      webElevacion = 0;
      webGiro = 0;
      debugSerial.println("SAFETY: USB link command timeout. Resetting motor intent to 0.");
    }
  }
}

void updateSimulatedPositions() {
  unsigned long now = millis();
  if (lastUpdate == 0) {
    lastUpdate = now;
    return;
  }
  float dt = (now - lastUpdate) / 1000.0; // en segundos
  lastUpdate = now;

  // Determinar la velocidad activa según el modo
  int currCarro = 0;
  int currElevacion = 0;
  int currGiro = 0;

  if (modoControlWeb) {
    currCarro = webCarro;
    currElevacion = webElevacion;
    currGiro = webGiro;
  } else {
    currCarro = readJoystick(JOY_X_PIN, MAX_VEL_CARRO);
    currElevacion = readJoystick(JOY_Y_PIN, MAX_VEL_ELEVACION);
    currGiro = readJoystick(JOY_Z_PIN, MAX_VEL_GIRO);
  }

  // Integrar Giro (velocidad de cambio: ~60 grados/seg a velocidad máx)
  if (currGiro != 0) {
    float rateGiro = 60.0 * (currGiro / (float)MAX_VEL_GIRO);
    posGiro += rateGiro * dt;
    // Normalizar ángulo entre -180 y 180 para que no crezca indefinidamente
    if (posGiro > 180.0) posGiro -= 360.0;
    if (posGiro < -180.0) posGiro += 360.0;
  }

  // Integrar Carro (velocidad de cambio: ~33.3 unidades/seg a velocidad máx)
  if (currCarro != 0) {
    float rateCarro = 33.3 * (currCarro / (float)MAX_VEL_CARRO);
    posCarro += rateCarro * dt;
    posCarro = constrain(posCarro, 65.0, 150.0);
  }

  // Integrar Gancho/Elevación
  // Elevación positiva es subir (U), lo que reduce la profundidad (posGancho)
  // Elevación negativa es bajar (D), lo que aumenta la profundidad (posGancho)
  if (currElevacion != 0) {
    float rateElev = 33.3 * (currElevacion / (float)MAX_VEL_ELEVACION);
    posGancho -= rateElev * dt;
    posGancho = constrain(posGancho, 0.0, 65.0);
  }
}

void sendTelemetry() {
  unsigned long now = millis();
  if (now - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = now;
    Serial.print("{\"giro\":");
    Serial.print(posGiro, 1);
    Serial.print(",\"carro\":");
    Serial.print(posCarro, 1);
    Serial.print(",\"gancho\":");
    Serial.print(posGancho, 1);
    Serial.println("}");
  }
}

void loop() {
  // Procesar comandos de la interfaz web / serial
  processUART();

  // Actualizar posiciones integradas
  updateSimulatedPositions();

  // Enviar telemetría JSON por hardware serial (USB)
  sendTelemetry();

  // Leer estado del botón de joystick con antirrebote (Debounce)
  bool btnState = digitalRead(JOY_BTN_PIN);
  if (btnState != lastBtnState) {
    if (millis() - lastBtnPressTime > DEBOUNCE_MS) {
      if (btnState == LOW) { // Botón pulsado (flanco de bajada)
        modoControlWeb = !modoControlWeb;
        // Enviar nuevo estado por UART de hardware (USB)
        Serial.write(modoControlWeb ? 'W' : 'M');
        // Enviar log explicativo
        debugSerial.print("BUTTON: Mode toggled physically. New mode: ");
        debugSerial.println(modoControlWeb ? "WEB" : "MANUAL");
        
        // Parar motores al cambiar de modo para evitar movimientos bruscos
        webCarro = 0; webElevacion = 0; webGiro = 0;
      }
      lastBtnPressTime = millis();
    }
    lastBtnState = btnState;
  }

  // Ejecución de movimientos según el modo activo
  if (modoControlWeb) {
    // Modo Web: Ejecutar comandos web
    controlMotorA(webCarro);
    controlMotorB(webElevacion);
    controlMotorC(webGiro);
  } else {
    // Modo Manual: Leer e intencionar joystick físico local
    int joyCarro = readJoystick(JOY_X_PIN, MAX_VEL_CARRO);
    int joyElevacion = readJoystick(JOY_Y_PIN, MAX_VEL_ELEVACION);
    int joyGiro = readJoystick(JOY_Z_PIN, MAX_VEL_GIRO);

    controlMotorA(joyCarro);
    controlMotorB(joyElevacion);
    controlMotorC(joyGiro);
  }
}
