import os
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHeaderView, QWidget, QPushButton
)

def ui_path(filename):
    # Returns the absolute path to the shared ui file at project root
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ui", filename))

class EventManagerStudent(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "EventManager-Student.ui"), self)

        # Wire common table sizing and signals via controller
        try:
            from controller.module6.event_manager_controller import wire_org_officer_signals
            wire_org_officer_signals(self, ui_path)
        except Exception as e:
            print(f"Error wiring Module 6 student signals: {e}")
            # Fallback: manually connect the attendance button
            if hasattr(self, "ViewAttendanceButton"):
                self.ViewAttendanceButton.clicked.connect(self.show_attendance_page)

        # Attendance will be lazy-loaded by the controller when needed

    def show_attendance_page(self):
        self.stackedWidget.setCurrentIndex(1)  # Show attendance page

    def show_main_page(self):
        self.stackedWidget.setCurrentIndex(0)  # Show main page

if __name__ == "__main__":
    app = QApplication([])
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    style_qss = os.path.join(project_root, "styles", "style.qss")
    if os.path.exists(style_qss):
        with open(style_qss, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    window = EventManagerStudent()
    window.show()
    app.exec()