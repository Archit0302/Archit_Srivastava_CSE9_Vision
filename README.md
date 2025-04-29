# Vision: Real-Time Motion Detection and Analysis

## 📌 Project Overview

**Vision** is a lightweight, real-time motion detection system developed using Python and OpenCV. It captures live video from a webcam, detects motion, classifies its intensity, identifies the direction and zone of movement, and logs every motion event with a timestamp.

This system is ideal for surveillance, smart monitoring, and motion-triggered event logging.

---

## 👨‍💻 Team Members

- **Archit Srivastava** – 2401410009  
- **Chanchal Yadav** – 2401410011  
- **Alishna** – 2401410013  
- **Chetna** – 2401410028  

---

## 🚀 Features

- ✅ Real-time motion detection via webcam  
- ✅ Motion intensity classification: `Small`, `Medium`, `Big`, `Extreme`  
- ✅ Direction detection: `Left`, `Right`, `Up`, `Down`  
- ✅ Zone detection (3x3 grid layout)  
- ✅ Timestamped logging of each motion event  
- ✅ Snapshot saving categorized by intensity  
- ✅ GUI overlay displaying time, motion count, intensity, direction, and zone

---

## 🛠️ Technologies Used

- **Python 3.x**
- **OpenCV** – for video processing  
- **NumPy** – for array operations  
- **Datetime** – for timestamps  
- **Winsound** – (optional) for motion-based sound alerts  
- **Threading, OS** – for file and event handling  

---

## 📂 Project Structure

Vision/ ├── motion4.py # Main application script ├── motion_log.txt # Log file for all motion events ├── Snapshots/ │ ├── Small/ │ ├── Medium/ │ ├── Big/ │ └── Extreme/ └── README.md # This file

---

## 🖥️ How It Works

1. Launch `motion4.py` — your webcam activates automatically.
2. The system processes video frames and detects changes between them.
3. Once motion is detected:
   - The motion is classified by area (`Small`, `Medium`, etc.)
   - The direction and zone are computed.
   - A log entry is created and a snapshot is saved.
4. When no motion is detected for a few frames, the snapshot is finalized and stored.

---

## 🧠 Future Improvements

- 📧 Email or Telegram alerts for detected motion  
- ☁️ Cloud backup for snapshots and logs  
- 🧍 Object recognition (e.g., person vs object) using deep learning  
- 📊 Web dashboard for real-time monitoring  
- 📱 Mobile app integration  
- ⏰ Time-based scheduling (e.g., night-only detection)

---

## ▶️ Getting Started

### Prerequisites

Make sure you have Python and the following libraries installed:

```bash
pip install opencv-python
(Optional, for Windows sound alerts):

bash
Copy
Edit
pip install winsound
Run the Script
bash
Copy
Edit
python motion4.py

----

📄 License
This project is for educational and academic purposes.

🙌 Acknowledgements
Thanks to OpenCV and the Python open-source community for enabling powerful computer vision tools accessible to everyone. ``
