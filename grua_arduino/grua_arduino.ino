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

// Parámetros de velocidad máxima configurable
#define MAX_VEL_CARRO 255
#define MAX_VEL_ELEVACION 255
#define MAX_VEL_GIRO 255

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
        break;
      case 'W':
        if (!modoControlWeb) {
          modoControlWeb = true;
          Serial.write('W');
        }
        break;
      case 'M':
        if (modoControlWeb) {
          modoControlWeb = false;
          Serial.write('M');
        }
        break;
    }
  }

  // Timeout de seguridad web: solo se aplica si está en modo Web
  if (modoControlWeb && (millis() - lastWebCmdTime > WEB_TIMEOUT_MS)) {
    webCarro = 0;
    webElevacion = 0;
    webGiro = 0;
  }
}

void loop() {
  // Procesar comandos de la interfaz web / serial
  processUART();

  // Leer estado del botón de joystick con antirrebote (Debounce)
  bool btnState = digitalRead(JOY_BTN_PIN);
  if (btnState != lastBtnState) {
    if (millis() - lastBtnPressTime > DEBOUNCE_MS) {
      if (btnState == LOW) { // Botón pulsado (flanco de bajada)
        modoControlWeb = !modoControlWeb;
        // Enviar nuevo estado por UART
        Serial.write(modoControlWeb ? 'W' : 'M');
        
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
