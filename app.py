from flask import Flask, render_template, request, jsonify, send_file
import cv2
import numpy as np
import os
import pickle
from datetime import datetime
import pandas as pd
import base64

app = Flask(__name__)

# ===================== CONFIG =====================
DATASET_FOLDER = 'dataset'
TRAINER_FILE = 'encodings/trainer.yml'
ATTENDANCE_FOLDER = 'Attendance'

# Create folders
os.makedirs(DATASET_FOLDER, exist_ok=True)
os.makedirs('encodings', exist_ok=True)
os.makedirs(ATTENDANCE_FOLDER, exist_ok=True)

# Initialize Face Recognizer
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load trainer if exists
if os.path.exists(TRAINER_FILE):
    recognizer.read(TRAINER_FILE)

# Student mapping
student_map = {}
if os.path.exists('encodings/student_map.pkl'):
    with open('encodings/student_map.pkl', 'rb') as f:
        student_map = pickle.load(f)

# ===================== UTILITY FUNCTIONS =====================
def save_student_map():
    with open('encodings/student_map.pkl', 'wb') as f:
        pickle.dump(student_map, f)

def mark_attendance(roll, name):
    today = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(ATTENDANCE_FOLDER, f"attendance_{today}.csv")
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=['Roll', 'Name', 'Time', 'Date'])
    
    if not df[(df['Roll'] == int(roll)) & (df['Date'] == today)].empty:
        return False, "Attendance already marked today!"
    
    new_entry = {
        'Roll': int(roll),
        'Name': name,
        'Time': datetime.now().strftime("%H:%M:%S"),
        'Date': today
    }
    
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(file_path, index=False)
    return True, "Attendance marked successfully!"

# ===================== ROUTES =====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.json
            name = data.get('name')
            roll = data.get('roll')
            images = data.get('images', [])

            if not name or not roll or len(images) < 5:
                return jsonify({'status': 'error', 'message': 'Name, Roll and at least 5 images required!'})

            student_map[roll] = name
            save_student_map()

            trained_faces = []
            for img_data in images:
                image_data = img_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                nparr = np.frombuffer(image_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                if frame is None: continue

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face_roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
                    trained_faces.append(face_roi)
                    break

            if len(trained_faces) > 0:
                labels = [int(roll)] * len(trained_faces)
                recognizer.update(trained_faces, np.array(labels))
                recognizer.save(TRAINER_FILE)

            return jsonify({'status': 'success', 'message': f'{name} registered successfully!'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})

    return render_template('register.html')

@app.route('/mark_attendance')
def mark_attendance_page():
    return render_template('mark_attendance.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    # (Keep your current recognize function here - the one with base64 decoding)
    # ... paste your working recognize function ...
    
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'status': 'error', 'message': 'No image received'})

        # Convert base64 image to OpenCV format
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({'status': 'error', 'message': 'Could not decode image'})

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) == 0:
            return jsonify({'status': 'error', 'message': 'No face detected'})

        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (200, 200))
            
            # Recognize face
            label, confidence = recognizer.predict(face_roi)
            
            # Lower confidence = better match (usually < 70-80 is good)
            if confidence < 80:
                roll = str(label)
                name = student_map.get(roll, "Unknown")
                
                success, msg = mark_attendance(roll, name)
                if success:
                    return jsonify({
                        'status': 'success',
                        'name': name,
                        'roll': roll,
                        'message': 'Attendance Marked Successfully!'
                    })
                else:
                    return jsonify({
                        'status': 'info',
                        'name': name,
                        'roll': roll,
                        'message': msg
                    })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Face not recognized. Please register first.'
                })

        return jsonify({'status': 'error', 'message': 'Recognition failed'})

    except Exception as e:
        print("Error in recognize:", str(e))
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/view_attendance')
def view_attendance():
    dates = [f.replace("attendance_", "").replace(".csv", "") 
             for f in os.listdir(ATTENDANCE_FOLDER) if f.endswith(".csv")]
    dates = sorted(dates, reverse=True)
    
    selected_date = request.args.get('date', datetime.now().strftime("%Y-%m-%d"))
    file_path = os.path.join(ATTENDANCE_FOLDER, f"attendance_{selected_date}.csv")
    
    records = pd.read_csv(file_path).to_dict('records') if os.path.exists(file_path) else []
    
    return render_template('view_attendance.html', dates=dates, selected_date=selected_date, records=records)

@app.route('/download_attendance')
def download_attendance():
    selected_date = request.args.get('date', datetime.now().strftime("%Y-%m-%d"))
    file_path = os.path.join(ATTENDANCE_FOLDER, f"attendance_{selected_date}.csv")
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=f"attendance_{selected_date}.csv")
    return "No record found!", 404

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
