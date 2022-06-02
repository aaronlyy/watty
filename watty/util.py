# util.py
from datetime import datetime

def timestamp_milli_to_datetime(timestamp) -> datetime:
    return datetime.fromtimestamp(timestamp / 1000)

def datetime_to_timestamp_milli(date: datetime) -> int:
    return date.timestamp() * 1000