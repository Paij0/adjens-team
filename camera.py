import cv2
import joblib
import face_recognition
import datetime
import RPi.GPIO as GPIO
import time

# Inisialisasi GPIO
GPIO.setmode(GPIO.BCM)
selenoid_pin = 21  # Ganti dengan nomor pin GPIO yang Anda gunakan
GPIO.setup(selenoid_pin, GPIO.OUT)

lamp_pin_20 = 20  # Ganti dengan nomor pin GPIO yang sesuai
lamp_pin_16 = 16  # Ganti dengan nomor pin GPIO yang sesuai
GPIO.setup(lamp_pin_20, GPIO.OUT)
GPIO.setup(lamp_pin_16, GPIO.OUT)

ds_factor = 0.6

MODEL_PATH = 'latihfile.pkl'
model = joblib.load(MODEL_PATH)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

label_to_name = {
    0: "Kazi",
    1: "Paijo",
    2: "kazi",
    3: "yanmaa",
    # Tambahkan entri lain sesuai dengan jumlah kelas yang ada
}

last_log_time = datetime.datetime.now()
log_interval = 3

class VideoCameraMasuk(object):
    def __init__(self, id):
        self.video = cv2.VideoCapture(id)
        frame_width = 360
        frame_height = 240
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        # backup data sebelumnya
        self.image = cv2.imread("blank.jpg")

    def __del__(self):
        self.video.release()

    def extract_face_encoding(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_image)

        if len(face_encodings) > 0:
            return face_encodings[0]

        return None

    def get_frame(self):
        global last_log_time
        user_data = []
        jpeg = ''
        success, image = self.video.read()
        if success:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                face_encoding = self.extract_face_encoding(roi_gray)

                if face_encoding is not None:
                    label = model.predict([face_encoding])[0]
                    name = label_to_name.get(label, "Unknown")
                    current_time = datetime.datetime.now()

                    time_diff = current_time - last_log_time
                    if time_diff.total_seconds() >= log_interval:
                        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                        print(f"{timestamp} - {name}")
                        last_log_time = current_time

                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(image, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    user_data.append([name, "Hadir", current_time.time()])
                    
                    GPIO.output(selenoid_pin, GPIO.HIGH)
                    print("Pintu Terbuka.")
                    time.sleep(5)  # Atur berapa lama 

                    # Mengendalikan lampu pada pin GPIO 20
                    GPIO.output(lamp_pin_20, GPIO.HIGH)  # Lampu nyala
                    GPIO.output(lamp_pin_16, GPIO.LOW)   # Lampu mati

                    GPIO.output(selenoid_pin, GPIO.LOW)
                    print("Pintu Terkunci.")

                    break
                else:
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(image, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            ret, jpeg = cv2.imencode('.jpg', image)
            self.image = jpeg #backup image
            return jpeg.tobytes(), user_data
        return self.image.tobytes(), None

class VideoCameraKeluar(object):
    def __init__(self, id):  
        self.video = cv2.VideoCapture(id)  
        frame_width = 360
        frame_height = 240
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        # backup data sebelumnya
        self.image = cv2.imread("blank.jpg")

    def __del__(self):
        self.video.release()

    def extract_face_encoding(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_image)

        if len(face_encodings) > 0:
            return face_encodings[0]

        return None

    def get_frame(self):
        global last_log_time
        user_data = []
        jpeg = ''
        success, image = self.video.read()
        if success:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                face_encoding = self.extract_face_encoding(roi_gray)

                if face_encoding is not None:
                    label = model.predict([face_encoding])[0]
                    name = label_to_name.get(label, "Unknown")
                    current_time = datetime.datetime.now()

                    time_diff = current_time - last_log_time
                    if time_diff.total_seconds() >= log_interval:
                        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                        print(f"{timestamp} - {name}")
                        last_log_time = current_time

                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)  
                    cv2.putText(image, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)  
                    user_data.append([name, "Pulang", current_time.time()])
                    
                    GPIO.output(selenoid_pin, GPIO.HIGH)
                    print("Pintu Terbuka.")
                    time.sleep(5)  

                    # Mengendalikan lampu pada pin GPIO 16
                    GPIO.output(lamp_pin_20, GPIO.LOW)  # Lampu mati
                    GPIO.output(lamp_pin_16, GPIO.HIGH)  # Lampu nyala

                    GPIO.output(selenoid_pin, GPIO.LOW)
                    print("Pintu Terkunci.")
                    break
                else:
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(image, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            
            ret, jpeg = cv2.imencode('.jpg', image)
            self.image = jpeg 
            return jpeg.tobytes(), user_data
        return self.image.tobytes(), None 

