import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QHeaderView
from datetime import datetime

class ScheduleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Tag role for controller visibility logic
        self.user_role = "student"
        # Example logged-in student id for personal schedule loading
        self.student_id = "2025-00001"
        # Example: this student is in 2nd Year; restrict YearBox to 1st-2nd
        self.student_year = "2nd Year"
        project_root = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            )
        )
        ui_path = os.path.abspath(
            os.path.join(project_root, "ui", "schedule.ui")
        )
        uic.loadUi(ui_path, self)

        # Wire signals via controller
        try:
            from controller.module3.schedule_controller import wire_schedule_signals
            wire_schedule_signals(self)
        except Exception:
            pass

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
project_root = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)
style_qss = os.path.join(project_root, "styles", "style.qss")
if os.path.exists(style_qss):
    with open(style_qss, 'r', encoding='utf-8') as f:
        app.setStyleSheet(f.read())
window = ScheduleWindow()
window.show()
app.exec()