#include <LiquidCrystal_I2C.h>
#define MAX_BUF 80
#ifndef I2C_ADDR
  #define I2C_ADDR 0x3F
#endif
#ifndef LCD_COLS
  #define LCD_COLS 20
#endif
#ifndef LCD_ROWS
  #define LCD_ROWS 4
#endif

LiquidCrystal_I2C lcd(I2C_ADDR, LCD_COLS, LCD_ROWS);

void clear_serial_buffer(char *buf) {
    memset(buf, ' ', MAX_BUF);
}

bool read_serial_buffer(char *buf) {
    if (Serial.available()) {
        Serial.readBytes(buf, MAX_BUF);
        return true;
    }
    return false;
}

void write_serial_buffer(char *buf, LiquidCrystal_I2C lcd) {
    lcd.clear();
    for (int x = 0; x < MAX_BUF; x++) {
        lcd.write(buf[x]);
    }
}

void setup() {
    lcd.init();
    lcd.backlight();
    Serial.begin(115200);
}

void loop() {
    char serialBuffer[MAX_BUF];

    if (read_serial_buffer(serialBuffer)) {
        write_serial_buffer(serialBuffer, lcd);
        clear_serial_buffer(serialBuffer);
    }
}
