#include <LiquidCrystal.h>

// ------------------------ LCD ------------------------
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// ------------------------ Sensores e Rele ------------------------
const int PINO_SENSOR = A0;
const int PINO_RELE = 10;

// ------------------------ Configurações ------------------------
const int LIMIAR_SECO = 30;              
const unsigned long TEMPO_REGA = 200;  
const unsigned long INTERVALO_API = 240000; 

unsigned long ultimo_api = 0;
int umidadeSolo = 0;

// ------------------------ Auxiliares ------------------------
void limparLinha(byte linha) {
  lcd.setCursor(0, linha);
  lcd.print("                "); 
  lcd.setCursor(0, linha);
}

// ------------------------ Rega ------------------------
void irrigar() {
  limparLinha(1);
  lcd.print("Regando...");
  delay(500);

  digitalWrite(PINO_RELE, LOW);

  unsigned long inicio = millis();
  while (millis() - inicio < TEMPO_REGA) {
    limparLinha(1);
    lcd.print("Regando...");
    delay(500);
  }

  digitalWrite(PINO_RELE, HIGH); 

  limparLinha(1);
  lcd.print("Rega concluida");
  delay(2000);
}

// ------------------------ Setup ------------------------
void setup() {
  pinMode(PINO_RELE, OUTPUT);
  digitalWrite(PINO_RELE, HIGH); 

  lcd.begin(16, 2);
  lcd.print("Horta Vertical");
  limparLinha(1);
  lcd.print("Inicializando");

  Serial.begin(115200);
  delay(2000);
}

// ------------------------ Loop ------------------------
void loop() {

  // ====== Leitura do sensor ======
  umidadeSolo = analogRead(PINO_SENSOR);
  umidadeSolo = map(umidadeSolo, 1023, 0, 0, 100);

  limparLinha(1);
  lcd.print("Umidade: ");
  lcd.print(umidadeSolo);
  lcd.print("%");
  delay(1000);

  // ====== MODO MANUAL VIA SERIAL ======
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "regar") {
      irrigar();
    }
  }

  // ====== CHAMADA AUTOMÁTICA À API ======
  if (millis() - ultimo_api >= INTERVALO_API) {

    ultimo_api = millis();
    limparLinha(1);
    lcd.print("Consultando...");
    delay(500);

    Serial.println("pedir_previsao");

    
    while (Serial.available()) Serial.read();

    String resposta = "";
    unsigned long inicio = millis();

    while (millis() - inicio < 5000) {
      if (Serial.available()) {
        char c = Serial.read();
        if (c == '\n') break;
        resposta += c;
      }
    }

    resposta.trim();

    // ====== Interpretação da resposta ======
    if (resposta == "API:sim") {
      limparLinha(1);
      lcd.print("Vai chover");
      delay(2000);
    }

    else if (resposta == "API:nao") {
      if (umidadeSolo < LIMIAR_SECO) {
        irrigar();
      } else {
        limparLinha(1);
        lcd.print("Solo umido");
        delay(2000);
      }
    }

    else {
      // Fallback local (API falhou)
      limparLinha(1);
      lcd.print("API falhou");
      delay(1000);

      if (umidadeSolo < LIMIAR_SECO) {
        irrigar();
      }
    }
  }

  // ====== Status em repouso ======
  if (umidadeSolo < LIMIAR_SECO) {
    limparLinha(1);
    lcd.print("Seco -> Regar");
  } else {
    limparLinha(1);
    lcd.print("Umido -> OK");
  }

  delay(3000);
}