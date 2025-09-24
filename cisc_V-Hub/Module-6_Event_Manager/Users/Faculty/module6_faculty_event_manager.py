import os
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHeaderView, QDialog
)

def ui_path(filename):
    # Returns the absolute path to the shared ui file at project root
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ui", filename))

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
        if hasattr(self, "ViewEventTimeline"):
            self.ViewEventTimeline.clicked.connect(self.open_event_timeline)

    def open_event_timeline(self):
        dialog = EventTimelineDialog(self)
        dialog.exec()

class RequestRescheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(ui_path("Request Event Reschedule.ui"), self)
        if hasattr(self, "ViewEventTimeline"):
            self.ViewEventTimeline.clicked.connect(self.open_event_timeline)

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

        # Wire signals via controller
        try:
            from controller.module6.event_manager_controller import wire_faculty_signals
            wire_faculty_signals(self, self.open_event_timeline, self.open_request_reschedule, self.open_request_proposal)
        except Exception:
            pass

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
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    style_qss = os.path.join(project_root, "styles", "style.qss")
    if os.path.exists(style_qss):
        with open(style_qss, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    window = FacultyWindow()
    window.show()
    app.exec()