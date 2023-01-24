#include <Wire.h>

void setup() {
  Wire.begin(0x20);
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  Wire.onReceive(receiveEvent);
}

void loop() {
  delay(100);
}

void receiveEvent(int howMany) {
  if (howMany == 5) {
    int zero_to_begin = Wire.read();
    int pixel = Wire.read();
    int r = Wire.read();
    int g = Wire.read();
    int b = Wire.read();
    
    Serial.print("Received Pixel Data!  => ");
    Serial.print(pixel);
    Serial.print(" ");
    Serial.print(r);
    Serial.print(" ");
    Serial.print(g);
    Serial.print(" ");
    Serial.print(b);
    Serial.println();
  }
  else {
    Serial.print("Failed. Received: ");
    Serial.print(howMany);
    Serial.println();
  }
}
