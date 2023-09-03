import cv2
import joblib
import face_recognition
import datetime
import time

# Load trained model
MODEL_PATH = 'latihfile.pkl'
model = joblib.load(MODEL_PATH)

# Load cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to extract face encodings using the face_recognition library
def extract_face_encoding(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_image)
    if len(face_encodings) > 0:
        return face_encodings[0]
    return None
    
# Dictionary to map label to name
label_to_name = {
    0: "dhifa",
    1: "Paijo",
    2: "kazi",
    3: "yanmaa",
    # Add more entries based on the number of classes
}

# Initialize cameras
frame0 = cv2.VideoCapture(0)
frame2 = cv2.VideoCapture(2)

# Set frame width and height
frame_width = 360
frame_height = 240
frame0.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
frame0.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
frame2.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
frame2.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# Function to save attendance data to log
def save_absensi_to_log(name, user_type, last_log_time):
    current_time = time.time()
    if current_time - last_log_time >= 60:
        with open('absensi.log', 'a') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - {user_type} {name}\n")
        last_log_time = current_time
    return last_log_time

last_log_time_in = time.time()
last_log_time_out = time.time()

state = False

while True:
    state = not state

    if state:
        ret0, img0 = frame0.read()
        if ret0:
            # Your face recognition code here
            gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                face_encoding = extract_face_encoding(roi_gray)

                if face_encoding is not None:
                    # Predict the face label using the trained model
                    label = model.predict([face_encoding])[0]

                    # Convert label to name using the dictionary
                    name = label_to_name.get(label, "Unknown")

                    # Draw rectangle and label on the face
                    cv2.rectangle(img0, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img0, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    # Save attendance to log with 1 minute delay
                    last_log_time_in = save_absensi_to_log(name, 'In', last_log_time_in)

            cv2.imshow('Camera 0', img0)
    else:
        ret2, img2 = frame2.read()
        if ret2:
            # Your face recognition code here
            gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                face_encoding = extract_face_encoding(roi_gray)

                if face_encoding is not None:
                    # Predict the face label using the trained model
                    label = model.predict([face_encoding])[0]

                    # Convert label to name using the dictionary
                    name = label_to_name.get(label, "Unknown")

                    # Draw rectangle and label on the face
                    cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img2, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    # Save attendance to log with 1 minute delay
                    last_log_time_out = save_absensi_to_log(name, 'Out', last_log_time_out)

            cv2.imshow('Camera 2', img2)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release cameras and close windows
frame0.release()
frame2.release()
cv2.destroyAllWindows()
