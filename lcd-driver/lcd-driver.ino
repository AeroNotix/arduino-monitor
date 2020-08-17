#include <LiquidCrystal_I2C.h>
#define MAX_BUF 80

char serialBuffer[MAX_BUF];
LiquidCrystal_I2C lcd(0x3F, 20, 4);

void clear_serial_buffer() {
    memset(serialBuffer, ' ', MAX_BUF);
}

bool read_serial_buffer() {
    if (Serial.available()) {
        Serial.readBytes(serialBuffer, MAX_BUF);
        return true;
    }
    return false;
}

void write_serial_buffer() {
    lcd.clear();
    for (int x = 0; x < MAX_BUF; x++) {
        lcd.write(serialBuffer[x]);
    }
    clear_serial_buffer();
}

void setup() {
    lcd.init();
    lcd.backlight();
    Serial.begin(115200);
    clear_serial_buffer();
}

void loop() {
    if (read_serial_buffer()) {
        write_serial_buffer();
    }
}
