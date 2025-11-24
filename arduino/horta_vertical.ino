#include <LiquidCrystal.h>

// Conexões do LCD
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Conexões dos sensores e atuadores
const int PINO_SENSOR = A0;
const int PINO_RELE   = 10;

// Configurações do sistema
int umidadeSolo = 0;
const int LIMIAR_SECO = 70;     // abaixo disso a terra é considerada seca
const unsigned long TEMPO_REGA = 8000; // 8 segundos
const unsigned long INTERVALO_CONSULTA = 3600000; // 1 hora

unsigned long ultimo_tempo = 0;

void setup() {
  pinMode(PINO_RELE, OUTPUT);
  digitalWrite(PINO_RELE, HIGH); // Relé desligado

  lcd.begin(16, 2);
  lcd.print(" Horta Inteligente ");

  Serial.begin(9600);
  delay(2000);
}

void loop() {

  // ==== LEITURA DA UMIDADE DO SOLO ====
  umidadeSolo = analogRead(PINO_SENSOR);
  umidadeSolo = map(umidadeSolo, 1023, 0, 0, 100);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Umidade:");
  lcd.print(umidadeSolo);
  lcd.print("%");

  delay(1000);

  // ======= A CADA 1 HORA =======
  if (millis() - ultimo_tempo >= INTERVALO_CONSULTA) {

    ultimo_tempo = millis();

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Consultando API");
    delay(1000);

    // Solicita previsão ao Python
    Serial.println("pedir_previsao");

    // Aguarda resposta
    unsigned long tempo_inicio = millis();
    String resposta = "";

    while (millis() - tempo_inicio < 5000) { // 5 segundos
      if (Serial.available()) {
        resposta = Serial.readStringUntil('\n');
        resposta.trim();
        break;
      }
    }

    if (resposta == "API:sim") {
      // Vai chover → NÃO IRRIGAR
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Vai chover!");
      lcd.setCursor(0, 1);
      lcd.print("Sem irrigacao");
      digitalWrite(PINO_RELE, HIGH);
      delay(3000);
    }
    else if (resposta == "API:nao") {
      // Não vai chover → IRRIGA
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Nao vai chover");
      lcd.setCursor(0, 1);
      lcd.print("Irrigando...");
      
      digitalWrite(PINO_RELE, LOW);   // Liga bomba
      delay(TEMPO_REGA);
      digitalWrite(PINO_RELE, HIGH);  // Desliga bomba

      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Irrigacao OK");
      delay(2000);
    }
    else {
      // Falha na API → usa somente sensor
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Erro API");

      if (umidadeSolo < LIMIAR_SECO) {
        lcd.setCursor(0, 1);
        lcd.print("Irrigando...");

        digitalWrite(PINO_RELE, LOW);
        delay(TEMPO_REGA);
        digitalWrite(PINO_RELE, HIGH);

      } else {
        lcd.setCursor(0, 1);
        lcd.print("Solo OK");
      }

      delay(2000);
    }
  }

  // ==== SEGURANÇA: CONTROLE PELO SENSOR ====
  if (umidadeSolo < LIMIAR_SECO) {
    lcd.setCursor(0, 1);
    lcd.print("Seco -> Rega ");
  } else {
    lcd.setCursor(0, 1);
    lcd.print("Umido -> OK  ");
  }

  delay(1500);
}