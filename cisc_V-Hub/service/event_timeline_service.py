from typing import Dict, List, Optional
from .json_paths import read_json_file, write_json_file


FILENAME = "event_timeline.json"


def load_timeline(event_name: Optional[str] = None) -> Dict:
    data = read_json_file(FILENAME) or {}
    if event_name:
        events = data.get("events", {})
        return {"eventName": event_name, "timeline": events.get(event_name, [])}
    return data if data else {"timeline": []}


def add_timeline_item(day: str, time: str, activity: str, event_name: Optional[str] = None) -> Dict:
    data = read_json_file(FILENAME) or {}
    item = {"day": day, "time": time, "activity": activity}
    if event_name:
        events = data.setdefault("events", {})
        lst = events.setdefault(event_name, [])
        lst.append(item)
    else:
        data.setdefault("timeline", []).append(item)
    write_json_file(FILENAME, data)
    return item


def items_for_day(day: str) -> List[Dict]:
    data = read_json_file(FILENAME) or {"timeline": []}
    return [i for i in data.get("timeline", []) if i.get("day") == day]

