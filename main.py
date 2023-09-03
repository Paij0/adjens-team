from flask import Flask, render_template, Response
from camera import VideoCameraMasuk, VideoCameraKeluar
import datetime

app = Flask(__name__)

# Inisialisasi data absensi
absensi = {}

@app.route('/')
def index():
    return render_template('index.html', absensi=absensi)

@app.route('/camera')
def absensi_func():
    return render_template('camera.html')

def gen_masuk(camera):
    while True:
        frame, user_data = camera.get_frame()
        if user_data:
            update_absensi(user_data)  # Panggil fungsi untuk memperbarui data absensi
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def gen_keluar(camera):
    while True:
        frame, user_data = camera.get_frame()
        if user_data:
            update_absensi(user_data)  # Panggil fungsi untuk memperbarui data absensi
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Fungsi untuk memperbarui data absensi
def update_absensi(user_data):
    global absensi
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for data in user_data:
        name = data[0]
        status = data[1]
        
        if name in absensi:
            absensi[name]["Waktu Keluar"] = current_time
            absensi[name]["Status Kepulangan"] = status
        else:
            absensi[name] = {
                "Waktu Masuk": current_time,
                "Status Kedatangan": status,
                "Waktu Keluar": "",
                "Status Kepulangan": ""
            }

@app.route('/video_feed_masuk')
def video_feed_masuk():
    return Response(gen_masuk(VideoCameraMasuk(0)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_keluar')
def video_feed_keluar():
    return Response(gen_keluar(VideoCameraKeluar(2)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
