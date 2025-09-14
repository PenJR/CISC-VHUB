import os
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHeaderView, QDialog
)

def ui_path(filename):
    # Returns the absolute path to the shared ui file
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ui", filename))

class AttendanceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(ui_path("Attendance.ui"), self)
        if hasattr(self, "tableWidget"):
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.tableWidget.resizeRowsToContents()
        if hasattr(self, "pushButton_4"):
            self.pushButton_4.clicked.connect(self.close)

class EventTimelineDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(ui_path("Event Timeline.ui"), self)
        if hasattr(self, "WeekTable_2"):
            self.WeekTable_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

class RequestProposalDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(ui_path("Request Event Proposal.ui"), self)
        if hasattr(self, "pushButton"):
            self.pushButton.clicked.connect(self.open_event_timeline)

    def open_event_timeline(self):
        dialog = EventTimelineDialog(self)
        dialog.exec()

class RequestRescheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(ui_path("Request Event Reschedule.ui"), self)
        if hasattr(self, "pushButton"):
            self.pushButton.clicked.connect(self.open_event_timeline)

    def open_event_timeline(self):
        dialog = EventTimelineDialog(self)
        dialog.exec()

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
        if hasattr(self, "tableWidget"):
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.tableWidget.resizeRowsToContents()

        # Connect navigation buttons
        if hasattr(self, "pushButton_3"):
            self.pushButton_3.clicked.connect(self.show_attendance_dialog)

    def show_attendance_dialog(self):
        dialog = AttendanceDialog(self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication([])
    window = EventManagerStudent()
    window.show()
    app.exec()