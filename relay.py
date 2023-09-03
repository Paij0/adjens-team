import RPi.GPIO as GPIO
import time

# Inisialisasi GPIO
GPIO.setmode(GPIO.BCM)
selenoid_pin = 21  # Ganti dengan nomor pin GPIO yang Anda gunakan
GPIO.setup(selenoid_pin, GPIO.OUT)


# Hidupkan pompa air
GPIO.output(selenoid_pin, GPIO.HIGH)
print("Pompa air dihidupkan.")
time.sleep(5)  # Atur berapa lama pompa harus dihidupkan

# Matikan pompa air
GPIO.output(selenoid_pin, GPIO.LOW)
print("Pompa air dimatikan.")

# Bersihkan GPIO saat selesai
GPIO.cleanup()
