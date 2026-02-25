#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo servo;

void centerText(String text, int row) {
  int len = text.length();
  int col = (16 - len) / 2;
  if (col < 0) col = 0;
  lcd.setCursor(col, row);
  lcd.print(text);
}

void setup() {
  lcd.init();
  lcd.backlight();

  servo.attach(9);        // Servo on pin 9
  servo.write(0);         // Locked position

  Serial.begin(9600);

  lcd.clear();
  centerText("Scan QR Code", 0);
}

void loop() {

  if (Serial.available()) {

    String data = Serial.readStringUntil('\n');
    data.trim();

    int commaIndex = data.indexOf(',');

    if (commaIndex != -1) {

      String name = data.substring(0, commaIndex);
      String status = data.substring(commaIndex + 1);

      lcd.clear();
      centerText(name, 0);
      centerText(status, 1);

      if (status == "On Time" || status == "Late") {
        servo.write(90);     // Unlock
        delay(3000);         // 3 seconds open
        servo.write(0);      // Lock again
      }

      delay(2000);

      lcd.clear();
      centerText("Scan QR Code", 0);
    }
  }
}
