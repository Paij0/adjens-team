import os
import cv2
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import joblib
import face_recognition

# Path ke folder dengan gambar wajah yang dikenali
KNOWN_FACES_DIR = 'latih wajah'

# Path untuk menyimpan model yang dilatih
MODEL_PATH = 'latihfile'

# Load wajah yang dikenali dan labelnya
def load_known_faces():
    known_faces = []
    known_names = []

    for name in os.listdir(KNOWN_FACES_DIR):
        if name == '.DS_Store':
            continue
        
        for filename in os.listdir(os.path.join(KNOWN_FACES_DIR, name)):
            if filename == '.DS_Store':
                continue
                
            image = cv2.imread(os.path.join(KNOWN_FACES_DIR, name, filename))
            face_encoding = extract_face_encoding(image)

            if face_encoding is not None:
                known_faces.append(face_encoding)
                known_names.append(name)

    return known_faces, known_names

# Ekstraksi vektor encoding wajah menggunakan library face_recognition
def extract_face_encoding(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_image)

    if len(face_encodings) > 0:
        return face_encodings[0]

    return None

# Memuat gambar wajah yang dikenali dan labelnya
known_faces, known_names = load_known_faces()

# Melatih model SVM (Support Vector Machine)
le = LabelEncoder()
labels = le.fit_transform(known_names)
svm = SVC(C=1.0, kernel='linear', probability=True)
svm.fit(known_faces, labels)

# Simpan model yang dilatih dalam format .pkl
joblib.dump(svm, MODEL_PATH + '.pkl')
