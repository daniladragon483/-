import shlex
import csv
import os
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
            raise ValueError("Недостаточно колонок")
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
            print(f"[LOG ERROR] {e}")
            return False

    def delete_item(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)

    def print_items(self):
        print("\n--- ТЕКУЩИЕ ДАННЫЕ КОНТЕЙНЕРА ---")
        for i, item in enumerate(self.items):
            print(f"[{i}] {item.date} | {item.location} | {item.value}°C | {item.rgb}")
        print("---------------------------------\n")

    def save_to_file(self, filepath):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for item in self.items:
                    f.write(f"{item.date.strftime('%Y.%m.%d')};{item.location};{item.value};{item.rgb}\n")
            return True
        except Exception as e:
            print(f"[LOG ERROR] {e}")
            return False

    def remove_by_condition(self, condition_str):
        try:
            parts = condition_str.strip().split()
            if len(parts) != 3:
                raise ValueError("Format: field operator value")
            
            field, operator, target_val = parts
            new_items = []
            
            for item in self.items:
                item_val = getattr(item, field)
                if isinstance(item_val, (float, int)):
                    target_val = float(target_val)
                
                match = False
                if operator == '<' and item_val < target_val: match = True
                elif operator == '>' and item_val > target_val: match = True
                elif operator == '==' and str(item_val) == str(target_val): match = True
                elif operator == '<=' and item_val <= target_val: match = True
                elif operator == '>=' and item_val >= target_val: match = True
                
                if not match:
                    new_items.append(item)
            
            self.items = new_items
            return True
        except Exception as e:
            print(f"[LOG ERROR] {e}")
            return False

    def execute_command(self, line):
        line = line.strip()
        if not line: return
        
        if line.startswith("ADD"):
            data_raw = line[4:].strip().replace(';', ' ')
            self.add_from_line(f"CMD {data_raw}")
        elif line.startswith("REM"):
            self.remove_by_condition(line[4:].strip())
        elif line.startswith("SAVE"):
            self.save_to_file(line[5:].strip())
        elif line.startswith("PRINT"):
            self.print_items()

    def execute_commands_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    self.execute_command(line)
            return True
        except Exception as e:
            print(f"[LOG ERROR] {e}")
            return False