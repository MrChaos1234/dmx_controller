#include <Wire.h>
#include <FastLED.h>

#define NUM_LEDS 10
#define DATA_PIN 6

#define I2C_ADRESS 0x30 // I2C Pins are  A4 and A5 on Arduino Nano

CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(9600);
  
  FastLED.addLeds<SK6812, DATA_PIN, BRG>(leds, NUM_LEDS); //BRG IS CORRECT FOR MY SK6812 MINI-E
  FastLED.clear();
  FastLED.show();
  Wire.begin(I2C_ADRESS);
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
  
//    Serial.print("Received Pixel Data!  => ");
//    Serial.print(pixel);
//    Serial.print(" ");
//    Serial.print(r);
//    Serial.print(" ");
//    Serial.print(g);
//    Serial.print(" ");
//    Serial.print(b);
//    Serial.println();

    setPixels(pixel, r, g, b);
    
  }
  else {
    Serial.print("Not received 5 (4 + null at start) bytes. Received: ");
    Serial.print(howMany);
    Serial.println();
  }
}

void setPixels(int pixel, int r, int b, int g) {
  leds[pixel] = CRGB(r, g, b);
  FastLED.show();
}
