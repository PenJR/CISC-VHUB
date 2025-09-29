import os
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHeaderView, QDialog, QWidget, QPushButton, QInputDialog, QTableWidgetItem
)

def ui_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ui", filename))

class EventTimelineDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(ui_path("Event Timeline.ui"), self)
        if hasattr(self, "WeekTable_2"):
            self.WeekTable_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Hook Add to persist with requested event name if available
        try:
            from service.event_timeline_service import add_timeline_item, load_timeline
            from service.event_proposal_service import list_proposals
        except Exception:
            add_timeline_item = None
            load_timeline = None
            list_proposals = None
        # Default to first saved proposal as the current event
        self._requested_event = None
        if list_proposals:
            proposals = list_proposals() or []
            if proposals:
                self._requested_event = proposals[0].get("eventName")
        if hasattr(self, "Event_Add") and add_timeline_item:
            self.Event_Add.clicked.connect(lambda: self._add_timeline(add_timeline_item))
        # Render existing timeline for current event
        if load_timeline and hasattr(self, "WeekTable_2") and self._requested_event:
            data = load_timeline(self._requested_event)
            self._render_timeline_table(data)

    def _add_timeline(self, add_func):
        table = getattr(self, "WeekTable_2", None)
        if table is None:
            return
        row = table.currentRow()
        col = table.currentColumn()
        if row < 0 or col < 0:
            return
        v_item = table.verticalHeaderItem(row)
        h_item = table.horizontalHeaderItem(col)
        time_label = v_item.text() if v_item else ""
        day_label = h_item.text() if h_item else ""
        if not time_label or not day_label:
            return
        text, ok = QInputDialog.getText(self, "Add Timeline Item", f"Activity for {day_label} @ {time_label}:")
        if not ok or not text.strip():
            return
        hhmm = self._to_24h(time_label)
        add_func(day_label, hhmm, text.strip(), self._requested_event)
        table.setItem(row, col, QTableWidgetItem(text.strip()))

    def _to_24h(self, label: str) -> str:
        try:
            from datetime import datetime
            dt = datetime.strptime(label.replace("\u200f", "").strip(), "%I:%M %p")
            return dt.strftime("%H:%M")
        except Exception:
            return label

    def _render_timeline_table(self, data):
        table = getattr(self, "WeekTable_2", None)
        if table is None:
            return
        items = data.get("timeline", [])
        for item in items:
            day = item.get("day")
            time = item.get("time")
            activity = item.get("activity", "")
            try:
                from datetime import datetime
                label = datetime.strptime(time, "%H:%M").strftime("%I:%M %p").lstrip("0")
            except Exception:
                label = time
            row = -1
            col = -1
            for r in range(table.rowCount()):
                vh = table.verticalHeaderItem(r)
                if vh and vh.text() == label:
                    row = r
                    break
            for c in range(table.columnCount()):
                hh = table.horizontalHeaderItem(c)
                if hh and hh.text() == day:
                    col = c
                    break
            if row >= 0 and col >= 0:
                table.setItem(row, col, QTableWidgetItem(activity))

class RequestProposalDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(ui_path("Request Event Proposal.ui"), self)
        if hasattr(self, "ViewEventTimeline"):
            self.ViewEventTimeline.clicked.connect(self._save_and_open_event_timeline)
        self._populate_dropdowns()

    def _populate_dropdowns(self):
        try:
            from service.events_metadata_service import load_buildings, load_rooms, load_organizers
        except Exception:
            return
        if hasattr(self, "comboBox"):
            self.comboBox.clear()
            for b in load_buildings():
                self.comboBox.addItem(b.get("name", ""), b.get("id"))
        def refresh_rooms():
            if not hasattr(self, "comboBox_3"):
                return
            self.comboBox_3.clear()
            sel_building_id = None
            if hasattr(self, "comboBox") and hasattr(self.comboBox, "currentData"):
                sel_building_id = self.comboBox.currentData()
            for r in load_rooms(sel_building_id):
                self.comboBox_3.addItem(r.get("name", ""))
        if hasattr(self, "comboBox") and hasattr(self.comboBox, "currentIndexChanged"):
            self.comboBox.currentIndexChanged.connect(lambda _: refresh_rooms())
        refresh_rooms()
        if hasattr(self, "comboBox_2"):
            self.comboBox_2.clear()
            for org in load_organizers():
                self.comboBox_2.addItem(org.get("name", ""), org.get("id"))

    def _save_and_open_event_timeline(self):
        try:
            from service.event_proposal_service import save_proposal, add_proposal
        except Exception:
            save_proposal = None
            add_proposal = None
        if save_proposal:
            payload = {
                "eventName": getattr(self.lineEdit, "text", lambda: "")(),
                "building": getattr(self.comboBox, "currentText", lambda: "")(),
                "description": getattr(self.lineEdit_2, "text", lambda: "")(),
                "date": getattr(self.dateEdit, "date", lambda: None)().toString("yyyy-MM-dd") if hasattr(self, "dateEdit") else "",
                "time": getattr(self.timeEdit, "time", lambda: None)().toString("HH:mm") if hasattr(self, "timeEdit") else "",
                "roomName": getattr(self.comboBox_3, "currentText", lambda: "")(),
                "organizer": getattr(self.comboBox_2, "currentText", lambda: "")(),
                "budget": getattr(self.doubleSpinBox, "value", lambda: 0.0)(),
            }
            save_proposal(payload)
            if add_proposal:
                add_proposal(payload)
        dialog = EventTimelineDialog(self)
        dialog.exec()

class RequestRescheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(ui_path("Request Event Reschedule.ui"), self)
        if hasattr(self, "ViewEventTimeline"):
            self.ViewEventTimeline.clicked.connect(self.open_event_timeline)
        self._populate_dropdowns()

    def open_event_timeline(self):
        dialog = EventTimelineDialog(self)
        dialog.exec()

    def _populate_dropdowns(self):
        try:
            from service.events_metadata_service import load_buildings, load_rooms, load_organizers
            from service.event_proposal_service import list_proposals, get_proposal_by_name
        except Exception:
            return
        if hasattr(self, "comboBox_4"):
            self.comboBox_4.clear()
            for p in list_proposals():
                name = p.get("eventName", "")
                if name:
                    self.comboBox_4.addItem(name)
            if hasattr(self.comboBox_4, "currentIndexChanged"):
                self.comboBox_4.currentIndexChanged.connect(lambda _: self._apply_selected_event(get_proposal_by_name))
        if hasattr(self, "comboBox"):
            self.comboBox.clear()
            for b in load_buildings():
                self.comboBox.addItem(b.get("name", ""), b.get("id"))
        def refresh_rooms():
            if not hasattr(self, "comboBox_3"):
                return
            self.comboBox_3.clear()
            sel_building_id = None
            if hasattr(self, "comboBox") and hasattr(self.comboBox, "currentData"):
                sel_building_id = self.comboBox.currentData()
            for r in load_rooms(sel_building_id):
                self.comboBox_3.addItem(r.get("name", ""))
        if hasattr(self, "comboBox") and hasattr(self.comboBox, "currentIndexChanged"):
            self.comboBox.currentIndexChanged.connect(lambda _: refresh_rooms())
        refresh_rooms()
        if hasattr(self, "comboBox_2"):
            self.comboBox_2.clear()
            for org in load_organizers():
                self.comboBox_2.addItem(org.get("name", ""), org.get("id"))

    def _apply_selected_event(self, get_proposal_by_name):
        if not hasattr(self, "comboBox_4"):
            return
        name = self.comboBox_4.currentText()
        if not name:
            return
        proposal = get_proposal_by_name(name) or {}
        if hasattr(self, "comboBox"):
            idx = self.comboBox.findText(proposal.get("building", ""))
            if idx >= 0:
                self.comboBox.setCurrentIndex(idx)
        if hasattr(self, "comboBox_3"):
            room_name = proposal.get("roomName", "")
            idx = self.comboBox_3.findText(room_name)
            if idx >= 0:
                self.comboBox_3.setCurrentIndex(idx)
        if hasattr(self, "comboBox_2"):
            idx = self.comboBox_2.findText(proposal.get("organizer", ""))
            if idx >= 0:
                self.comboBox_2.setCurrentIndex(idx)
        try:
            if hasattr(self, "dateEdit") and proposal.get("date"):
                from PyQt6.QtCore import QDate
                y, m, d = [int(x) for x in proposal["date"].split("-")]
                self.dateEdit.setDate(QDate(y, m, d))
            if hasattr(self, "timeEdit") and proposal.get("time"):
                from PyQt6.QtCore import QTime
                hh, mm = [int(x) for x in proposal["time"].split(":")]
                self.timeEdit.setTime(QTime(hh, mm))
        except Exception:
            pass

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

        # Attendance will be lazy-loaded by the controller when needed

        # Wire common table sizing and signals via controller
        try:
            from controller.module6.event_manager_controller import wire_org_officer_signals
            wire_org_officer_signals(self, ui_path)
        except Exception:
            pass

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
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    style_qss = os.path.join(project_root, "styles", "style.qss")
    if os.path.exists(style_qss):
        with open(style_qss, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    window = OrgOfficerWindow()
    window.show()
    app.exec()