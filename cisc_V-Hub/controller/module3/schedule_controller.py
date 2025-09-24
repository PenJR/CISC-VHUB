from PyQt6.QtWidgets import QPushButton, QStackedWidget


def wire_schedule_signals(window: object) -> None:
    # Button connections
    if hasattr(window, "viewCurriculum") and hasattr(window, "show_curriculum_page"):
        window.viewCurriculum.clicked.connect(window.show_curriculum_page)
    if hasattr(window, "Return") and hasattr(window, "show_schedule_page"):
        window.Return.clicked.connect(window.show_schedule_page)

    # Optional: ensure stacked widget navigation exists
    if hasattr(window, "stackedWidget") and isinstance(window.stackedWidget, QStackedWidget):
        pass


