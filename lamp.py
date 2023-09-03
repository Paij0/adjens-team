import RPi.GPIO as GPIO
import time

# Inisialisasi GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Tentukan nomor pin untuk lampu LED
lampu1_pin = 20
lampu2_pin = 16

# Atur pin sebagai output
GPIO.setup(lampu1_pin, GPIO.OUT)
GPIO.setup(lampu2_pin, GPIO.OUT)

try:
    while True:
        # Nyalakan lampu 1, matikan lampu 2
        GPIO.output(lampu1_pin, GPIO.HIGH)
        GPIO.output(lampu2_pin, GPIO.LOW)
        time.sleep(1)  # Tunggu selama 1 detik

        # Matikan lampu 1, nyalakan lampu 2
        GPIO.output(lampu1_pin, GPIO.LOW)
        GPIO.output(lampu2_pin, GPIO.HIGH)
        time.sleep(1)  # Tunggu selama 1 detik

except KeyboardInterrupt:
    # Tangkap KeyboardInterrupt (Ctrl+C) untuk menghentikan program
    print("Program dihentikan oleh pengguna.")
finally:
    # Setel semua pin GPIO ke mode default
    GPIO.cleanup()
