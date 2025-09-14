import os
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHeaderView, QDialog
)

def ui_path(filename):
    # Returns the absolute path to the shared ui file
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ui", filename))

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

class AttendanceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(ui_path("Attendance.ui"), self)
        if hasattr(self, "tableWidget"):
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.tableWidget.resizeRowsToContents()
        if hasattr(self, "pushButton_4"):
            self.pushButton_4.clicked.connect(self.close)

class FacultyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "EventManager-Faculty.ui"), self)

        # Make all table columns fit the table width and rows fit contents
        for table_name in [
            "PendingTable", "Events_table_3", "Events_table_4",
            "Events_table_6", "Events_table_7", "tableWidget"
        ]:
            table = getattr(self, table_name, None)
            if table:
                table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
                table.resizeRowsToContents()

        # Connect buttons to open dialogs
        if hasattr(self, "pushButton_10"):
            self.pushButton_10.clicked.connect(self.open_event_timeline)
        if hasattr(self, "pushButton_19"):
            self.pushButton_19.clicked.connect(self.open_request_reschedule)
        if hasattr(self, "pushButton_3"):
            self.pushButton_3.clicked.connect(self.open_request_proposal)

    def open_event_timeline(self):
        dialog = EventTimelineDialog(self)
        dialog.exec()

    def open_request_proposal(self):
        dialog = RequestProposalDialog(self)
        dialog.exec()

    def open_request_reschedule(self):
        dialog = RequestRescheduleDialog(self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication([])
    window = FacultyWindow()
    window.show()
    app.exec()