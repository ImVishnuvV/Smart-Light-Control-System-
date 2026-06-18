An automated gesture light control system using Computer Vision and Ardunio NANO 
Decription :


An intelligent home automation project that uses Computer Vision and Arduino to control light brightness based on user presence and hand gestures.



- Person Detection using OpenCV
- Hand Gesture Recognition using MediaPipe
- Automatic Light ON/OFF based on presence
- Brightness Control using Finger Gestures
- Smooth Brightness Transition
- Audio Greeting when a person is detected
- Audio Alert when no person is detected



- Python
- OpenCV
- MediaPipe
- Arduino Nano
- PySerial
- Pygame

- Arduino Nano
- LED
- Resistor
- USB Cable
- Webcam
- Computer/Laptop



| Fingers Detected | Brightness |
|------------------|------------|
| 0 | OFF (0) |
| 1 | 50 |
| 2 | 127 |
| 3 | 180 |
| 5 | 255 |


```
AI-Home-Automation-System
│
├── python project.py
├── sketch_jul15a.ino
├── requirements.txt
├── README.md
└── .gitignore
```



1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Home-Automation-System.git
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Upload the Arduino code to Arduino Nano.

4. Update the COM port in Python file:

```python
arduino = serial.Serial('COM4', 9600)
```

5. Run the project:

```bash
python "python project.py"
```

## Future Improvements

- Fan Speed Control
- Mobile Application Integration
- Voice Assistant Support
- IoT Dashboard
- Smart Energy Monitoring

## Author

Vishnu V

Electrical and Electronics Engineering Student

Passionate about AI, IoT, Automation and Software Development
