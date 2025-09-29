from PyQt6.QtWidgets import QPushButton, QStackedWidget, QTableWidget, QTableWidgetItem
from datetime import datetime

# Services
try:
    from service.schedule_service import load_schedule
    from service.curriculum_service import load_curriculum
except Exception:
    load_schedule = lambda student_id=None: {}
    load_curriculum = lambda year_name=None: {}


def wire_schedule_signals(window: object) -> None:
    # Button connections
    if hasattr(window, "viewCurriculum") and hasattr(window, "show_curriculum_page"):
        window.viewCurriculum.clicked.connect(window.show_curriculum_page)
    if hasattr(window, "Return") and hasattr(window, "show_schedule_page"):
        window.Return.clicked.connect(window.show_schedule_page)

    # Search and semester change
    if hasattr(window, "Search") and hasattr(window, "StudentSearch"):
        # Hide search for students
        role = getattr(window, "user_role", "faculty")
        if role == "student":
            try:
                window.Search.setVisible(False)
                window.StudentSearch.setVisible(False)
            except Exception:
                pass
        else:
            window.Search.clicked.connect(lambda: _populate_schedule(window))
    if hasattr(window, "Semester"):
        try:
            window.Semester.currentIndexChanged.connect(lambda _=None: _populate_today(window))
        except Exception:
            pass
    if hasattr(window, "YearBox"):
        try:
            window.YearBox.currentIndexChanged.connect(lambda _=None: _populate_curriculum(window))
        except Exception:
            pass

    # Initial populate
    _populate_schedule(window)

    # Optional: ensure stacked widget navigation exists
    if hasattr(window, "stackedWidget") and isinstance(window.stackedWidget, QStackedWidget):
        pass


# --- Helpers ---

_DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
_TIMES_DISPLAY = [
    "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM",
    "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM",
    "5:00 PM", "6:00 PM", "7:00 PM",
]


def _format_time_display(hhmm: str) -> str:
    try:
        dt = datetime.strptime(hhmm, "%H:%M")
        return dt.strftime("%#I:%M %p") if hasattr(datetime, "strftime") else dt.strftime("%I:%M %p").lstrip("0")
    except Exception:
        return hhmm


def _populate_schedule(window: object) -> None:
    data = load_schedule(getattr(window, "StudentSearch").text() if hasattr(window, "StudentSearch") else None)
    _populate_weekly_table(getattr(window, "WeekTable_2", None), data)
    _populate_today(window)
    _populate_curriculum(window)


def _populate_weekly_table(table: QTableWidget | None, schedule: dict) -> None:
    if not table or not isinstance(table, QTableWidget):
        return
    # Ensure table has expected dimensions (rows follow _TIMES_DISPLAY, columns follow _DAYS)
    table.setRowCount(len(_TIMES_DISPLAY))
    table.setColumnCount(len(_DAYS))
    for r, label in enumerate(_TIMES_DISPLAY):
        item = QTableWidgetItem(label)
        table.setVerticalHeaderItem(r, item)
    for c, day in enumerate(_DAYS):
        item = QTableWidgetItem(day)
        table.setHorizontalHeaderItem(c, item)

    weekly = schedule.get("weekly", {}) if isinstance(schedule, dict) else {}
    # Clear cells
    for r in range(len(_TIMES_DISPLAY)):
        for c in range(len(_DAYS)):
            table.setItem(r, c, QTableWidgetItem(""))

    # Fill
    for day, entries in weekly.items():
        if day not in _DAYS:
            continue
        c = _DAYS.index(day)
        for entry in entries:
            time_disp = _format_time_display(entry.get("time", ""))
            if time_disp not in _TIMES_DISPLAY:
                continue
            r = _TIMES_DISPLAY.index(time_disp)
            text = f"{entry.get('subject', '')} ({entry.get('room', '')})"
            table.setItem(r, c, QTableWidgetItem(text))


def _populate_today(window: object) -> None:
    table = getattr(window, "tableWidget_2", None)
    if not table or not isinstance(table, QTableWidget):
        return
    schedule = load_schedule(getattr(window, "StudentSearch").text() if hasattr(window, "StudentSearch") else None)
    today = schedule.get("today", []) if isinstance(schedule, dict) else []
    # Mirror _TIMES_DISPLAY rows
    table.setRowCount(len(_TIMES_DISPLAY))
    table.setColumnCount(1)
    for r, label in enumerate(_TIMES_DISPLAY):
        item = QTableWidgetItem(label)
        table.setVerticalHeaderItem(r, item)
        table.setItem(r, 0, QTableWidgetItem(""))
    for entry in today:
        time_disp = _format_time_display(entry.get("time", ""))
        if time_disp in _TIMES_DISPLAY:
            r = _TIMES_DISPLAY.index(time_disp)
            text = f"{entry.get('subject', '')} ({entry.get('room', '')})"
            table.setItem(r, 0, QTableWidgetItem(text))


def _populate_curriculum(window: object) -> None:
    year_name = None
    if hasattr(window, "YearBox") and hasattr(window.YearBox, "currentText"):
        year_name = window.YearBox.currentText()
    cur = load_curriculum(year_name)
    sem1 = getattr(window, "sem1", None)
    sem2 = getattr(window, "sem2frame", None)
    if not (isinstance(sem1, QTableWidget) and isinstance(sem2, QTableWidget)):
        return
    semesters = cur.get("semesters", []) if isinstance(cur, dict) else []
    _fill_semester_table(sem1, next((s for s in semesters if s.get("name") == "1st Semester"), {"subjects": []}))
    _fill_semester_table(sem2, next((s for s in semesters if s.get("name") == "2nd Semester"), {"subjects": []}))


def _fill_semester_table(table: QTableWidget, sem: dict) -> None:
    headers = ["Codes", "Subject Title", "Grades", "Units", "Pre-requisite(s)"]
    table.setColumnCount(len(headers))
    for c, h in enumerate(headers):
        table.setHorizontalHeaderItem(c, QTableWidgetItem(h))
    subjects = sem.get("subjects", [])
    table.setRowCount(len(subjects))
    for r, subj in enumerate(subjects):
        table.setItem(r, 0, QTableWidgetItem(subj.get("code", "")))
        table.setItem(r, 1, QTableWidgetItem(subj.get("title", "")))
        table.setItem(r, 2, QTableWidgetItem(str(subj.get("grade", ""))))
        table.setItem(r, 3, QTableWidgetItem(str(subj.get("units", ""))))
        prereq = ", ".join(subj.get("prerequisites", []) or [])
        table.setItem(r, 4, QTableWidgetItem(prereq))


