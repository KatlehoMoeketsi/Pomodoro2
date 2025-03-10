import os.path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget,
    QListWidgetItem, QStackedWidget, QFrame
)

from PyQt6.QtCore import Qt, QSize, QTimer, QUrl
from PyQt6.QtGui import QIcon, QFont
import sys
import os
import pygame




def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def create_about_page():
    page = QWidget()
    layout = QVBoxLayout(page)
    label = QLabel("This is a Pomodoro timer to help with focus and productivity")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label)
    return page

class PomodoroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        pygame.mixer.quit()
        pygame.mixer.init()


        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.is_work_session = True
        self.timer_remaining =25 * 60
        self.short_break = 5 * 60
        self.long_break = 15 * 60
        self.timer_running = False
        self.session_count = 0 #Track Pom Cycles

        #Global widgets
        self.play_button = None
        self.timer_label = None

        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Pomodoro-Beta")
        self.setWindowIcon(QIcon("tom.ico"))
        self.setGeometry(100, 100, 800, 500)

        # Main container
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)  # Use QVBoxLayout for top-to-bottom layout
        self.setCentralWidget(main_widget)

        # Set the background color to pastel white (light grayish-white)
        main_widget.setStyleSheet("background-color: #f7f7f7;")  # Pastel white background color

        # Sidebar (Navigation)
        sidebar_layout = QHBoxLayout()  # Horizontal layout for sidebar and main content
        self.nav_list = QListWidget()
        self.nav_list.setFixedWidth(200)
        self.nav_list.addItem(QListWidgetItem("Pomodoro"))
        self.nav_list.addItem(QListWidgetItem("About"))
        self.nav_list.addItem(QListWidgetItem("Settings"))
        self.nav_list.clicked.connect(self.switch_page)

        # Stack for switching pages
        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_pomodoro_page())
        self.stack.addWidget(self.create_about_page())
        self.stack.addWidget(self.create_settings_page())

        # Add sidebar and content stack to layout
        sidebar_layout.addWidget(self.nav_list)
        sidebar_layout.addWidget(self.stack)

        main_layout.addLayout(sidebar_layout)

    def switch_page(self):
        """Switch pages based on sidebar selection."""
        self.stack.setCurrentIndex(self.nav_list.currentRow())

    def next_session(self):
        #Switch Session
        if self.timer:
            print("Timer is running")
            self.timer.stop()#End timer

            #Switch the timer manually
            # Switch between work and break cycles
            self.switch_session()
            # Update the UI immediately
            self.timer_label.setText(self.format_time(self.timer_remaining))
            self.play_button.setIcon(QIcon(resource_path("assets/pause.svg")))

            # Automatically restart timer
            self.timer_running = True
            self.timer.start(1000)

    def create_pomodoro_page(self):
        """Creates the Pomodoro page layout."""
        page = QWidget()
        layout = QVBoxLayout(page)
        header_label = QLabel("Pomodoro timer")

        header_label.setStyleSheet("font-size:42px; font-weight: bold; color: #4CAF50;padding:20px;")

        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)

        self.session_label = QLabel("Click Play button to start!")
        self.session_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.session_label.setStyleSheet("font-size: 36px; font-weight: normal;")
        layout.addWidget(self.session_label)

        #timer_frame is the rounded timer card - timer card uses a Qframe, basically a square of some kind
        timer_frame = QFrame()
        #We can use setStyleSheet and CSS coding to customize our elements
        timer_frame.setStyleSheet("Background-color:#e3e1e1; border-radius: 10px; padding: 20px; ")
        #timer_frame is our container,a.k.a, our timer card, now we set the height
        timer_frame.setFixedHeight(150)
        #Now we set a layout within the timer, i think.
        timer_layout = QVBoxLayout(timer_frame)

        self.timer_label = QLabel("--:--")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 42px; font-weight: bold;")
        timer_layout.addWidget(self.timer_label)

        #Button Card added below the Timer Card
        button_frame = QFrame()
        button_frame.setStyleSheet("background-color: #e3e1e1; border-radius: 10px; padding: 15px;")
        button_frame.setFixedHeight(120)
        button_layout= QHBoxLayout(button_frame)

        refresh_button = QPushButton()
        refresh_button.setIcon(QIcon(resource_path("assets/refresh.svg")))
        refresh_button.clicked.connect(self.reset_timer)
        refresh_button.setIconSize(QSize(48, 48))

        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon(resource_path("assets/play.svg")))
        self.play_button.setIconSize(QSize(48, 48))
        self.play_button.clicked.connect(self.toggle_timer)

        next_button = QPushButton()
        next_button.setIcon(QIcon(resource_path("assets/next.svg")))
        next_button.setIconSize(QSize(48, 48))
        next_button.clicked.connect(self.next_session)


        for btn in [refresh_button, self.play_button, next_button]:
            btn.setFixedSize(60, 40)
            btn.setStyleSheet("background-color: #4CAF50;color: white; border-radius:10px font-size: 50px")

        button_layout.addWidget(refresh_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(next_button)

        #finally add widgets to the layout
        layout.addWidget(timer_frame)
        layout.addWidget(button_frame)
        return page

    def start_timer(self):
        if not self.timer_running: #prevent multiple timers running at once
            self.timer.start(1000) #update every 1 second
            self.timer_running = True

    def toggle_timer(self):
        if self.timer_running:
            self.timer.stop()
            self.play_button.setIcon(QIcon(resource_path("assets/play.svg")))
            self.session_label.setText("Paused")
        else:
            self.timer.start(1000)
            self.play_button.setIcon(QIcon(resource_path("assets/pause.svg")))
            self.session_label.setText("Work!")
        self.timer_running = not self.timer_running

    def reset_timer(self):
        self.timer.stop()
        self.timer_remaining = 25 * 60 #reset to 25 minutes
        self.timer_label.setText("--:--")
        self.timer_running = False
        self.session_label.setText("Click Play button to start!")
        self.play_button.setIcon(QIcon(resource_path("assets/play.svg")))

    def update_timer(self):
        """update timer to display every second"""
        if self.timer_remaining > 0:
            self.timer_remaining -=1
            self.timer_label.setText(self.format_time(self.timer_remaining))
        else:
            self.timer.stop()
            self.timer_running = False
            self.timer_label.setText(self.format_time(self.timer_remaining))
            self.play_button.setIcon(QIcon(resource_path("assets/play.svg")))

            self.switch_session()

            #Update the UI immediately
            self.timer_label.setText(self.format_time(self.timer_remaining))
            self.play_button.setIcon(QIcon(resource_path("assets/pause.svg")))

            # Automatically restart timer
            self.timer_running = True
            self.timer.start(1000)

    def switch_session(self):
        # Switch between work and break cycles
        if self.is_work_session:
            self.session_count += 1
            if self.session_count % 4 == 0:
                play_sound("assets/break_start.wav")
                self.timer_remaining = self.long_break  # long break every 4 sessions
                self.session_label.setText("Long Break")

            else:
                play_sound("assets/break_start.wav")
                self.timer_remaining = self.short_break  # Short break
                self.session_label.setText("Short Break")

            self.is_work_session = False
        else:
            play_sound("assets/work_start.wav")
            self.timer_remaining = 25 * 60
            self.is_work_session = True
            self.session_label.setText("Work Time")

    @staticmethod
    def format_time(seconds):
        """ Format seconds into MM:SS """
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"


    def create_about_page(self):
        page = QWidget()
        #Then create a layout object of type QVBoxLayout which receives an object of type QWidget
         # Layout
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)  # Add some padding
        layout.setSpacing(20)  # Space between elements

        # Title Label
        title_label = QLabel("About the Pomodoro Technique")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Description Text
        description = """
               The Pomodoro Technique is a time management method that breaks work into 25-minute 
               sessions called 'Pomodoros', followed by short 5-minute breaks. After four Pomodoros, 
               take a longer break of 15-30 minutes. 

               This cycle helps improve focus, reduce burnout, and boost productivity.
               """
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 12))
        desc_label.setWordWrap(True)  # Allows text to wrap properly
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        return page

    def create_settings_page(self):
        #Start by declaring a page object of type QWidget
        page = QWidget()
        #Then create a layout object of type QVBoxLayout which receives an object of type QWidget
        layout = QVBoxLayout(page)
        """ We've just created the following:
         1. A page
         2. Defined a layout
         3. Now we will start adding the elements"""

        return page


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PomodoroApp()
    window.show()
    sys.exit(app.exec())
