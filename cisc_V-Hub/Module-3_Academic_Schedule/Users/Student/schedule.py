import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QHeaderView
from datetime import datetime

class ScheduleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "schedule.ui")
        uic.loadUi(ui_path, self)

        # Connect buttons to page switching
        self.viewCurriculum.clicked.connect(self.show_curriculum_page)
        self.Return.clicked.connect(self.show_schedule_page)

        # Ensure all QTableWidgets' columns fit the table width
        self.WeekTable_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sem1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sem2frame.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set labelTodayHeader_2 to today's day name
        today_name = datetime.now().strftime("%A")
        self.labelTodayHeader_2.setText(today_name)

    def show_curriculum_page(self):
        self.stackedWidget.setCurrentIndex(1)  # Curriculum page

    def show_schedule_page(self):
        self.stackedWidget.setCurrentIndex(0)  # Schedule page

app = QApplication([])
with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'styles', 'style.qss'), 'r') as f:
    app.setStyleSheet(f.read())
window = ScheduleWindow()
window.show()
app.exec()