
from datetime import datetime
import uuid
from Client import Client
from Transaction import Transaction



class AuditLog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            self.buffer = []
            self.max_buffer = 100
            self.log_file = "audit.log"
            self._initialized = True

    def log(self, level, message, event_type, timestamp=datetime.now(),
            user_id="", details=None):
        details = details or {}
        log = AuditLogEntry(level, message, event_type, timestamp, user_id, details)
        if len(self.buffer) >= self.max_buffer:
            delete_from_buffer = self.buffer[0]
            self.buffer.pop(0)
            self.save_to_file(delete_from_buffer)
        if level == "CRITICAL":
            self.save_to_file(log)
        
        self.buffer.append(log)

    # CHECKED OK
    def get_recent_logs(self, count):
        recenet_logs = self.buffer[(len(self.buffer))-count:]
        return recenet_logs
    
    def filter_logs(self, filter:dict):
        
        filter_for_logs = {}
        for item in filter.items():
            key, value = item
            filter_for_logs[key] = value
        filtered_logs = [item for item in self.buffer
                         if all(item.to_dict().get(key) == value for key, value in filter_for_logs.items())]
        return filtered_logs
        
        

    def save_to_file(self, log):
        import os
        import json
        from pathlib import Path

        date_now = datetime.now()
        data = {
            'log': log.to_dict()
        }

        filepath = './logs/AuditLog.json'

        # Создаем директорию, если ее нет
        Path('./logs').mkdir(parents=True, exist_ok=True)

        # Читаем существующие данные
        existing_data = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    existing_data = json.load(file)
                    # Убедимся, что это список
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data] if existing_data else []
            except:
                existing_data = []

        # Добавляем новую ошибку
        existing_data.append(data)

        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(existing_data, file, ensure_ascii=False, indent=2)
            print(f"✅ Лог сохранен в {filepath}")
        except Exception as e:
            print(f"❌ Ошибка сохранения в файл {filepath}: {e}")

    def clear_buffer(self):
        self.buffer.clear()
        


class AuditLogEntry:
    def __init__(self, level, message, event_type, timestamp=datetime.now(), user_id='', details=None) -> None:
        self.id: str = str(uuid.uuid4())[:8].upper()
        self.timestamp: datetime = timestamp
        self.level: str = level
        self.message: str = message
        self.event_type: str = event_type
        self.user_id: str = user_id
        self.details = details or {}

        if self.id is None:
            self.id = str(uuid.uuid4())[:8].upper()

    def to_dict(self):
        return{
            "ID": self.id,
            "Time": self.timestamp.strftime("%d.%m.%Y %H:%M:%S"),
            "Level": self.level,
            "Message": self.message,
            "Event type": self.event_type,
            "User ID": self.user_id,
            "Details": self.details
        }


if __name__ == "__main__":
    pass