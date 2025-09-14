import os
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHeaderView, QDialog, QWidget, QPushButton
)

def ui_path(filename):
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

class OrgOfficerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "EventManager-OrgOfficer.ui"), self)

        # Load Attendance.ui into the attendance page (page_2) in the stacked widget
        attendance_widget = QWidget()
        uic.loadUi(ui_path("Attendance.ui"), attendance_widget)
        self.stackedWidget.removeWidget(self.stackedWidget.widget(1))  # Remove the empty page_2
        self.stackedWidget.insertWidget(1, attendance_widget)
        self.attendance_page = attendance_widget

        # Connect "View Attendance" button to show attendance page
        if hasattr(self, "ViewAttendanceButton"):
            self.ViewAttendanceButton.clicked.connect(self.show_attendance_page)

        # Connect Go Back button in attendance page
        go_back_btn = self.attendance_page.findChild(QPushButton, "pushButton_4")
        if go_back_btn:
            go_back_btn.clicked.connect(self.show_main_page)

        # Make all table columns fit the table width and rows fit contents
        for table_name in [
            "PendingTable", "Events_table_3", "Events_table_4",
            "Events_table_6", "Events_table_7", "tableWidget"
        ]:
            table = getattr(self, table_name, None)
            if table:
                table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
                table.resizeRowsToContents()

        # Connect new dialog buttons
        if hasattr(self, "RequestRescheduleButton"):
            self.RequestRescheduleButton.clicked.connect(self.open_request_reschedule)
        if hasattr(self, "RequestEventProposalButton"):
            self.RequestEventProposalButton.clicked.connect(self.open_request_proposal)

    def show_attendance_page(self):
        self.stackedWidget.setCurrentIndex(1)  # Show attendance page

    def show_main_page(self):
        self.stackedWidget.setCurrentIndex(0)  # Show main page

    def open_event_timeline(self):
        dialog = EventTimelineDialog(self)
        dialog.exec()

    def open_request_proposal(self):
        dialog = RequestProposalDialog(self)
        dialog.exec()

    def open_request_reschedule(self):
        dialog = RequestRescheduleDialog(self)
        dialog.exec()

    def open_attendance_dialog(self):
        dialog = AttendanceDialog(self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication([])
    window = OrgOfficerWindow()
    window.show()
    app.exec()