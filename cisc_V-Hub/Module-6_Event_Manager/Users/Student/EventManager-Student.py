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

        # Make all table columns fit the table width
        if hasattr(self, "EventT_Table"):
            self.EventT_Table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.EventT_Table.resizeRowsToContents()
        if hasattr(self, "Events_table"):
            self.Events_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.Events_table.resizeRowsToContents()

        # --- Load Attendance.ui into the empty page_2 of the stacked widget ---
        attendance_widget = QWidget()
        uic.loadUi(ui_path("Attendance.ui"), attendance_widget)
        self.stackedWidget.removeWidget(self.stackedWidget.widget(1))  # Remove the empty page_2
        self.stackedWidget.insertWidget(1, attendance_widget)
        self.attendance_page = attendance_widget

        # Connect "View Attendance" button to show attendance page
        if hasattr(self, "pushButton_3"):
            self.pushButton_3.clicked.connect(self.show_attendance_page)

        # Connect Go Back button in attendance page
        go_back_btn = self.attendance_page.findChild(QPushButton, "pushButton_4")
        if go_back_btn:
            go_back_btn.clicked.connect(self.show_main_page)

    def show_attendance_page(self):
        self.stackedWidget.setCurrentIndex(1)  # Show attendance page

    def show_main_page(self):
        self.stackedWidget.setCurrentIndex(0)  # Show main page

if __name__ == "__main__":
    app = QApplication([])
    window = EventManagerStudent()
    window.show()
    app.exec()