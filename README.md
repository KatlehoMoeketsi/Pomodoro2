📌 Pomodoro Timer App
A simple yet powerful Pomodoro Timer built with PyQt6, featuring a clean UI, session tracking, and sound alerts.

🚀 Features
✅ Pomodoro Timer – Work & break cycles to boost productivity
✅ Customizable Sessions – Work, short break, and long break options
✅ Automatic Session Switching – No need to restart after each session
✅ Sound Notifications – Alerts when switching between sessions
✅ Sidebar Navigation – Access Pomodoro, About, and Settings
✅ Modern UI – Styled with QSS for a sleek look

🛠 Installation
🔹 Prerequisites
Ensure you have Python 3.9+ installed.

🔹 Clone the Repository
git clone https://github.com/yourusername/pomodoro-timer.git
cd pomodoro-timer

🔹 Install Dependencies
pip install -r requirements.txt

▶️ Usage
Run the app with:
python main.py

or if using the Windows EXE:
./PomodoroTimer.exe

📦 Dependencies
PyQt6 (GUI Framework)
pygame (For sound alerts)

To install required dependencies manually:
pip install PyQt6 pygame

🛠 Building an Executable (.exe)
To package the app into an executable:
pyinstaller --onefile --windowed --name "PomodoroTimer" --icon=icons/timer.ico main.py
Make sure to include your assets folder when distributing the EXE.

This project is open-source under the MIT License.


