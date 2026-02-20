import shlex
from datetime import datetime

class TemperatureMeasurement:
    def __init__(self, date_str, location, value, rgb):
        try:
            self.date = datetime.strptime(date_str, "%Y.%m.%d").date()
            self.location = location
            self.value = float(value)
            self.rgb = str(rgb)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Ошибка в данных: {e}")

    @staticmethod
    def from_line(line):
        parts = shlex.split(line)
        if len(parts) < 5:
            raise ValueError("Недостаточно колонок в строке")
        return TemperatureMeasurement(parts[1], parts[2], parts[3], parts[4])

class MeasurementModel:
    def __init__(self):
        self.items = []

    def add_from_line(self, line):
        try:
            new_obj = TemperatureMeasurement.from_line(line)
            self.items.append(new_obj)
            return True
        except Exception as e:
            print(f"[LOG ERROR] Некорректная строка: {e}")
            return False