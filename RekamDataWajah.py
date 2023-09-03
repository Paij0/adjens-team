import cv2
import os

# Path lengkap ke berkas cascade classifier
CASCADE_PATH = '/home/adjens-team/Paijo-SIC/haarcascade_frontalface_default.xml'

# Nama folder untuk menyimpan gambar wajah
FACES_FOLDER = 'latih wajah'

# Nama pengguna untuk identifikasi wajah yang diambil
username = input("Masukkan no absen pengguna: ")

# Buat folder untuk menyimpan gambar wajah
user_folder = os.path.join(FACES_FOLDER, username)
os.makedirs(user_folder, exist_ok=True)

# Mulai pengambilan gambar
camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

count = 0
while True:
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        roi = frame[y:y+h, x:x+w]
        roi_gray = gray[y:y+h, x:x+w]

        # Simpan gambar wajah ke dalam folder
        image_path = os.path.join(user_folder, f'{count}.jpg')
        cv2.imwrite(image_path, roi_gray)
        count += 1

    cv2.imshow('Capture Face', frame)

    # Menghentikan pengambilan gambar setelah 50 gambar wajah diambil
    if count >= 50:
        break

    # Menghentikan pengambilan gambar dengan menekan tombol 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
