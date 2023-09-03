import cv2
import joblib
import face_recognition
import datetime

# Path untuk model yang dilatih
MODEL_PATH = 'latihfile.pkl'

# Load model yang dilatih
model = joblib.load(MODEL_PATH)

# Load cascade classifier untuk deteksi wajah
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Fungsi untuk ekstraksi vektor encoding wajah menggunakan library face_recognition
def extract_face_encoding(image):
    # Menggunakan face_recognition library untuk ekstraksi vektor encoding
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_image)

    if len(face_encodings) > 0:
        return face_encodings[0]

    return None

# Dictionary untuk memetakan label ke nama
label_to_name = {
    0: "Kazi",
    1: "Paijo",
    2: "kazi",
    3: "yanmaa",
    # Tambahkan entri lain sesuai dengan jumlah kelas yang ada
}

# Inisialisasi waktu terakhir penulisan log
last_log_time = datetime.datetime.min

# Interval waktu untuk penulisan log (dalam detik)
log_interval = 60  # Misalnya, interval 1 menit

# Mulai pengenalan wajah menggunakan webcam
camera = cv2.VideoCapture(2)

while True:
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        face_encoding = extract_face_encoding(roi_gray)

        if face_encoding is not None:
            # Memprediksi label wajah menggunakan model yang dilatih
            label = model.predict([face_encoding])[0]

            # Mengubah label menjadi nama menggunakan dictionary
            name = label_to_name.get(label, "Unknown")

            # Mendapatkan waktu saat ini
            current_time = datetime.datetime.now()

            # Memeriksa interval waktu untuk penulisan log
            time_diff = current_time - last_log_time
            if time_diff.total_seconds() >= log_interval:
                # Simpan absensi ke file log
                with open('absensi.log', 'a') as f:
                    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"{timestamp} - {name}\n")

                # Update waktu terakhir penulisan log
                last_log_time = current_time

            # Menandai wajah dengan kotak dan label
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        else:
            # Menandai wajah dengan kotak dan label "Unknown"
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow('Face Recognition', frame)

    # Menghentikan pengenalan wajah dengan menekan tombol 'q' atau 'esc'
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:  # 'q' atau 'esc'
        break

camera.release()
cv2.destroyAllWindows()
