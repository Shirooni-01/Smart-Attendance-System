# 🎓 Smart Attendance System using Face Recognition

A web-based attendance management system that uses **real-time face recognition** to automatically mark student attendance.

This project is built with **Flask**, **OpenCV**, and **Pandas**. It captures student face samples during registration, trains a local LBPH recognizer, and saves daily attendance records to CSV files.

---

## ✨ Features

- Register new students with face samples directly from the browser
- Real-time face recognition via webcam/image capture
- Automatic attendance marking with duplicate prevention for the same day
- View attendance records by date
- Download attendance history as CSV
- Simple file-based storage using CSV and pickle
- Lightweight Flask application with minimal dependencies

---

## 🛠️ Tech Stack

- Python
- Flask
- OpenCV
- NumPy
- Pandas
- HTML / Bootstrap / JavaScript

---

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/smart-attendance-system.git
   cd smart-attendance-system
   ```

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Run the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

---

## 📌 How It Works

1. **Register Student**
   - Go to `/register`
   - Enter student name and roll number
   - Upload or capture at least 5 face images
   - The application saves the face encodings and trains the recognizer

2. **Mark Attendance**
   - Go to `/mark_attendance`
   - Use the webcam interface to capture a live face image
   - The system recognizes the student and marks attendance if not already present for today

3. **View Attendance**
   - Go to `/view_attendance`
   - Choose a date to see attendance records for that day
   - Download records as CSV using the download button

---

## 📁 Project Structure

- `app.py` - Main Flask application and face recognition logic
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates for web pages
- `static/` - CSS and client-side assets
- `attendance/` - Generated attendance CSV files
- `dataset/` - Captured student face images (optional)
- `encodings/` - Trained recognizer files and student mapping
- `instance/` - Flask instance folder (if used)
- `model.py`, `utils.py` - placeholder modules for future extensions

---

## 📂 Data Storage

- `encodings/trainer.yml` - trained LBPH recognizer model
- `encodings/student_map.pkl` - saved map of roll numbers to student names
- `attendance/attendance_YYYY-MM-DD.csv` - daily attendance logs

---

## ✅ Notes

- The app uses OpenCV Haar Cascade for face detection and LBPH for recognition.
- Attendance is prevented from being added more than once per student per day.
- If a student is not recognized, they should be registered first.

---

## 💡 Improvements

Possible future enhancements include:

- Add a proper database (SQLite/MySQL)
- Improve model training and recognition accuracy
- Add admin authentication
- Add support for bulk student import
- Add a dashboard for analytics and attendance summaries

---

## 📄 License

This project is available under the MIT License. Feel free to reuse and extend it.

