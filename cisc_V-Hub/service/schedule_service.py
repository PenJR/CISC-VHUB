from typing import Dict, List, Optional
from .json_paths import read_json_file, write_json_file


FILENAME = "schedule.json"


def load_schedule(student_id: Optional[str] = None) -> Dict:
    data = read_json_file(FILENAME) or {}
    if not student_id:
        return data
    if data.get("studentId") == student_id:
        return data
    return {}


def search_classes_by_day(day: str) -> List[Dict]:
    data = read_json_file(FILENAME) or {}
    weekly = data.get("weekly", {})
    return weekly.get(day, [])


def add_class(day: str, time: str, subject: str, room: str) -> Dict:
    data = read_json_file(FILENAME) or {}
    if "weekly" not in data:
        data["weekly"] = {}
    if day not in data["weekly"]:
        data["weekly"][day] = []
    new_item = {"time": time, "subject": subject, "room": room}
    data["weekly"][day].append(new_item)
    write_json_file(FILENAME, data)
    return new_item

