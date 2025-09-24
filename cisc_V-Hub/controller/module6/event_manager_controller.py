from PyQt6.QtWidgets import QHeaderView, QWidget, QPushButton
from PyQt6 import uic


def wire_org_officer_signals(window: object, ui_path_func) -> None:
    # Connect to the updated object name from UI: ViewAttendanceButton
    if hasattr(window, "ViewAttendanceButton"):
        window.ViewAttendanceButton.clicked.connect(lambda: _load_and_show_attendance(window, ui_path_func))

    # Fit various tables if present
    for table_name in [
        "PendingTable", "Events_table_3", "Events_table_4",
        "Events_table_6", "Events_table_7", "tableWidget",
        "EventT_Table", "Events_table"
    ]:
        table = getattr(window, table_name, None)
        if table and hasattr(table, "horizontalHeader"):
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            if hasattr(table, "resizeRowsToContents"):
                table.resizeRowsToContents()


def wire_faculty_signals(window: object, open_timeline, open_reschedule, open_proposal) -> None:
    # Updated object names from UI: RequestEventProposalButton, RequestRescheduleButton
    if hasattr(window, "RequestEventProposalButton"):
        window.RequestEventProposalButton.clicked.connect(open_proposal)
    if hasattr(window, "RequestRescheduleButton"):
        window.RequestRescheduleButton.clicked.connect(open_reschedule)


def _show_page(window: object, index: int) -> None:
    if hasattr(window, "stackedWidget"):
        window.stackedWidget.setCurrentIndex(index)


def _load_and_show_attendance(window: object, ui_path_func) -> None:
    # Lazy-load Attendance.ui into index 1 if not already present
    if not hasattr(window, "attendance_page") or window.attendance_page is None:
        attendance_widget = QWidget()
        uic.loadUi(ui_path_func("Attendance.ui"), attendance_widget)
        # If there is already a widget at index 1, replace it; otherwise insert
        if hasattr(window, "stackedWidget"):
            if window.stackedWidget.count() > 1:
                window.stackedWidget.removeWidget(window.stackedWidget.widget(1))
                window.stackedWidget.insertWidget(1, attendance_widget)
            else:
                window.stackedWidget.insertWidget(1, attendance_widget)
        window.attendance_page = attendance_widget
        # Wire Go Back button inside the newly loaded page
        go_back_btn = attendance_widget.findChild(QPushButton, "pushButton_4")
        if go_back_btn:
            go_back_btn.clicked.connect(lambda: _show_page(window, 0))

    _show_page(window, 1)


