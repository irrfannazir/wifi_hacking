import time
import RPi.GPIO as GPIO
from i2c_lcd import I2cLcd  # Assuming you're using this library

# GPIO Pin Definitions
BUTTON_UP = 17
BUTTON_DOWN = 27
BUTTON_SELECT = 22

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LCD Setup
I2C_ADDR = 0x27  # Update this address if necessary
I2C_BUS = 1
lcd = I2cLcd(I2C_BUS, I2C_ADDR, 2, 16)  # 16x2 LCD

def read_button(pin):
    return GPIO.input(pin) == GPIO.LOW  # Button pressed

def lcd_menu(item_list):
    index = 0
    first_visible = 0
    max_visible_lines = 2
    total_items = len(item_list)

    def refresh_display():
        lcd.clear()
        # Show two items starting from first_visible
        for i in range(max_visible_lines):
            item_idx = first_visible + i
            if item_idx >= total_items:
                break
            prefix = "> " if item_idx == index else "  "
            lcd.move_to(0, i)
            item_text = item_list[item_idx][:14]  # 14 because prefix takes 2 spaces
            lcd.putstr(f"{prefix}{item_text}")

    refresh_display()

    while True:
        if read_button(BUTTON_UP):
            if index > 0:
                index -= 1
                if index < first_visible:
                    first_visible -= 1
                refresh_display()
                time.sleep(0.2)  # Debounce delay

        elif read_button(BUTTON_DOWN):
            if index < total_items - 1:
                index += 1
                if index >= first_visible + max_visible_lines:
                    first_visible += 1
                refresh_display()
                time.sleep(0.2)

        elif read_button(BUTTON_SELECT):
            lcd.clear()
            lcd.putstr("Selected:")
            lcd.move_to(0, 1)
            lcd.putstr(item_list[index][:16])
            time.sleep(1)
            lcd.clear()
            return index

        time.sleep(0.05)  # Polling delay

