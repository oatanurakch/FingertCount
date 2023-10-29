int LED[5] = { 27, 26, 25, 33, 32 };

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(50);
  for (byte i = 0; i < 5; i++) {
    pinMode(LED[i], OUTPUT);
  }
}

void loop() {
  while (Serial.available()) {
    int count = Serial.readString().toInt();
    for(byte i = 0; i < count; i++){
      digitalWrite(LED[i], HIGH);
    }
    for(byte j = count; j < 5; j++){
      digitalWrite(LED[j], LOW);
    }
  }
}
