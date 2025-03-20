import smbus
import time
import subprocess
import re

# I2C LCD SETUP
I2C_ADDR = 0x27   # Update based on i2cdetect result
LCD_WIDTH = 16

LCD_CHR = 1
LCD_CMD = 0

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

LCD_BACKLIGHT = 0x08

ENABLE = 0b00000100
E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(1)  # Use 1 for newer Raspberry Pi

# Initialize LCD
def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)

def lcd_message(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

def display_password(password):
    lcd_init()
    lcd_message("KEY FOUND!", LCD_LINE_1)
    lcd_message(password, LCD_LINE_2)
    print(f"Displayed password: {password}")

# Run Aircrack-ng and capture output
def run_aircrack():
    # Customize this command!
    command = [
        "aircrack-ng",
        "capture.hccapx",              # Your capture file
        "-w", "../wordlist/rockyou.txt"          # Your wordlist file   
    ]

    try:
        # Start aircrack-ng process
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Loop over output lines as they come
        for line in iter(process.stdout.readline, ''):
            print(line.strip())  # Optional: view progress in terminal

            # Look for the line containing 'KEY FOUND!'
            if "KEY FOUND!" in line:
                # Extract the password using regex
                match = re.search(r"KEY FOUND!\s+\[\s*(.+?)\s*\]", line)
                if match:
                    password = match.group(1)
                    display_password(password)
                    break  # Stop after finding the key

        process.stdout.close()
        process.wait()

    except KeyboardInterrupt:
        print("Process interrupted by user.")
    except Exception as e:
        print(f"Error running aircrack-ng: {e}")

if __name__ == '__main__':
    run_aircrack()
