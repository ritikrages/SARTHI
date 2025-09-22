#include <Arduino.h>

// TODO: Wire actual pins and modules (LCD, buzzer, relay, lights)
// Pins (example)
const int PIN_BUZZER = 8;
const int PIN_RELAY = 7; // Immobilize relay
const int PIN_FLASH = 6; // Flash lights

void setup() {
  Serial.begin(9600);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_RELAY, OUTPUT);
  pinMode(PIN_FLASH, OUTPUT);
  digitalWrite(PIN_BUZZER, LOW);
  digitalWrite(PIN_RELAY, LOW);
  digitalWrite(PIN_FLASH, LOW);
}

void flashLights(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(PIN_FLASH, HIGH);
    delay(200);
    digitalWrite(PIN_FLASH, LOW);
    delay(200);
  }
}

void hornBeep(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(PIN_BUZZER, HIGH);
    delay(300);
    digitalWrite(PIN_BUZZER, LOW);
    delay(200);
  }
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "FLASH") {
      flashLights(6);
      Serial.println("{\"ok\":true,\"ack\":\"FLASH\"}");
    } else if (cmd == "HORN") {
      hornBeep(3);
      Serial.println("{\"ok\":true,\"ack\":\"HORN\"}");
    } else if (cmd == "IMMOBILIZE") {
      // SAFETY: immobilization requires legal review and safe conditions
      digitalWrite(PIN_RELAY, HIGH);
      Serial.println("{\"ok\":true,\"ack\":\"IMMOBILIZE\"}");
    } else if (cmd == "SOS") {
      flashLights(10);
      hornBeep(5);
      Serial.println("{\"ok\":true,\"ack\":\"SOS\"}");
    } else {
      Serial.println("{\"ok\":false,\"error\":\"UNKNOWN\"}");
    }
  }
}


